import ssl
import email
import logging
from imapclient import IMAPClient
from imapclient.exceptions import LoginError
from imapclient.response_types import BodyData

from django.conf import settings
from django.utils import module_loading

from papermerge.core.import_pipeline import IMAP
from papermerge.core.models import User


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


def read_email_message(message, user=None):
    """
    message is an instance of python's module email.message
    """
    for _, part in enumerate(message.walk()):
        # search for payload
        try:
            pipelines = settings.PAPERMERGE_PIPELINES
            # TODO: 100% as local.py and views/document.py
            # Please, refactor
            init_kwargs = {'payload': part, 'processor': IMAP}
            apply_kwargs = {'user': user, 'name': part.get_filename()}
            for pipeline in pipelines:
                pipeline_class = module_loading.import_string(pipeline)
                try:
                    importer = pipeline_class(**init_kwargs)
                except Exception as e:
                    # please use fstrings
                    logger.debug("{} importer: {}".format("IMAP", e))
                    importer = None
                if importer is not None:
                    try:
                        # is apply function supposed to return something?
                        # please document
                        importer.apply(**apply_kwargs)
                        # what is the purpose if get_init_kwargs?
                        # what is it supposed to return?
                        # please document/comment
                        init_kwargs_temp = importer.get_init_kwargs()
                        # what is the purpose of get_apply_kwargs?
                        # what is it supposed to return?
                        # please document/comment
                        apply_kwargs_temp = importer.get_apply_kwargs()
                        if init_kwargs_temp:
                            init_kwargs = {**init_kwargs, **init_kwargs_temp}
                        if apply_kwargs_temp:
                            apply_kwargs = {
                                **apply_kwargs, **apply_kwargs_temp}
                    except Exception as e:
                        # please use fstrings
                        logger.error("{} importer: {}".format("IMAP", e))
                        continue
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
            if isinstance(
                structure[8],
                tuple
            ) and structure[8][0] == b'attachment':
                return True
        except IndexError:
            return False
    return False


def import_attachment():
    imap_server = settings.PAPERMERGE_IMPORT_MAIL_HOST
    username = settings.PAPERMERGE_IMPORT_MAIL_USER
    password = settings.PAPERMERGE_IMPORT_MAIL_PASS
    by_user = settings.PAPERMERGE_IMPORT_MAIL_BY_USER
    by_secret = settings.PAPERMERGE_IMPORT_MAIL_BY_SECRET
    delete = settings.PAPERMERGE_IMPORT_MAIL_DELETE

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
            imported = False
            user = None
            body = message_data[b'RFC822']
            sender = message_data[b'ENVELOPE'].from_[0]
            sender_address = '{}@{}'.format(sender.mailbox.decode(),
                                            sender.host.decode())
            try:
                message_secret = body.split(b'SECRET{')[1].split(b'}')[0]
            except IndexError:
                message_secret = None
            body = message_data[b'RFC822']
            email_message = email.message_from_bytes(
                body
            )

            # Priority to sender address
            if by_user:
                user = User.objects.filter(
                    email=sender_address
                ).first()
                logger.debug("Found user {}".format(user))
            if user:
                if user.mail_by_user:
                    read_email_message(email_message, user=user)
                    imported = True

            # Then check secret
            if not imported and by_secret and message_secret is not None:
                user = User.objects.filter(
                    mail_secret=message_secret
                ).first()
            if user:
                if user.mail_by_secret:
                    read_email_message(email_message, user=user)
                    imported = True

            # Otherwise put it into first superuser's inbox
            if not imported:
                read_email_message(email_message)
                imported = True

        if delete:
            server.delete_messages(messages)

    else:
        logger.info(
            f"IMAP import: Failed to login to imap server {imap_server}."
            " Please double check IMAP account credentials."
        )
