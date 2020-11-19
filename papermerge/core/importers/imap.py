import ssl
import email
import tempfile
import logging
from django.conf import settings
from imapclient import IMAPClient
from imapclient.exceptions import LoginError
from imapclient.response_types import BodyData

from django.utils import module_loading

logger = logging.getLogger(__name__)


def login(imap_server, username, password):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    server = IMAPClient(
        imap_server,
        ssl_context=ssl_context
    )

    try:
        server.login(username, password)
    except LoginError:
        logger.error(
            "IMAP Import: ERROR. Login failed."
        )
        return None

    return server


def read_email_message(message):
    """
    message is an instance of python's module email.message
    """
    for index, part in enumerate(message.walk()):
        # search for payload
        try:
            pipelines = settings.PAPERMERGE_PIPELINES
            for pipeline in pipelines:
                pipeline_class = module_loading.import_string(pipeline)
                importer = pipeline_class(payload=part, processor="IMAP")
                doc = importer.apply(user=None, name=part.get_filename())
        except TypeError:
            continue


def contains_attachments(uid, structure):
    if isinstance(structure, BodyData):
        if structure.is_multipart:
            for part in structure:
                if isinstance(part, list):
                    for element in part:
                        if contains_attachments(uid, element):
                            return True
        try:
            if isinstance(structure[8], tuple) and structure[8][0] == b'attachment':
                return True
        except IndexError:
            return False
    return False


def import_attachment():
    imap_server = settings.PAPERMERGE_IMPORT_MAIL_HOST
    username = settings.PAPERMERGE_IMPORT_MAIL_USER
    password = settings.PAPERMERGE_IMPORT_MAIL_PASS

    server = login(
        imap_server=imap_server,
        username=username,
        password=password
    )

    if server:
        server.select_folder(settings.PAPERMERGE_IMPORT_MAIL_INBOX)
        messages = server.search(['UNSEEN'])

        logger.debug(
            f"IMAP Import: UNSEEN messages {len(messages)} count"
        )

        messages_structure = server.fetch(messages, ['BODYSTRUCTURE'])
        for uid, structure in messages_structure.items():
            if not contains_attachments(uid, structure[b'BODYSTRUCTURE']):
                messages.remove(uid)

        for uid, message_data in server.fetch(
            messages, ['ENVELOPE', 'RFC822']
        ).items():
            body = message_data[b'RFC822']
            email_message = email.message_from_bytes(
                body
            )
            read_email_message(email_message)
    else:
        logger.info(
            f"IMAP import: Failed to login to imap server {imap_server}."
            " Please double check IMAP account credentials."
        )
