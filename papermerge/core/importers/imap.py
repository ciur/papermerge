import ssl
import email
import logging
from imapclient import IMAPClient
from imapclient.exceptions import LoginError
from imapclient.response_types import BodyData

from django.conf import settings

from papermerge.core.import_pipeline import IMAP, go_through_pipelines
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
    for part in message.iter_attachments():
        try:
            payload = part.get_content()
        except KeyError:
            continue
        init_kwargs = {'payload': payload, 'processor': IMAP}
        apply_kwargs = {'user': user, 'name': part.get_filename()}
        go_through_pipelines(init_kwargs, apply_kwargs)


def contains_attachments(structure):
    if isinstance(structure, BodyData):
        if structure.is_multipart:
            for part in structure:
                if isinstance(part, list):
                    for element in part:
                        if contains_attachments(element):
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


def extract_info_from_email(email_message):
    by_user = settings.PAPERMERGE_IMPORT_MAIL_BY_USER
    by_secret = settings.PAPERMERGE_IMPORT_MAIL_BY_SECRET
    extracted_by_user = False
    user = None
    user_found = None

    sender_address = email.utils.parseaddr(
        email_message.get('From'))[1]
    try:
        message_secret = email_message.as_string().split(
            'SECRET{')[1].split('}')[0]
    except IndexError:
        message_secret = None

    # Priority to sender address
    if by_user:
        user_found = User.objects.filter(
            email=sender_address
        ).first()
        logger.debug(f"{IMAP} importer: found user {user_found} from email")
    if user_found and user_found.mail_by_user:
        user = user_found
        extracted_by_user = True

    # Then check secret
    if not extracted_by_user and by_secret and message_secret is not None:
        user_found = User.objects.filter(
            mail_secret=message_secret
        ).first()
        logger.debug(f"{IMAP} importer: found user {user_found} from secret")
    if user_found and user_found.mail_by_secret:
        user = user_found

    # Otherwise put it into first superuser's inbox

    return user


def import_attachment():
    imap_server = settings.PAPERMERGE_IMPORT_MAIL_HOST
    username = settings.PAPERMERGE_IMPORT_MAIL_USER
    password = settings.PAPERMERGE_IMPORT_MAIL_PASSc
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
            if not contains_attachments(structure[b'BODYSTRUCTURE']):
                messages.remove(uid)

        for uid, message_data in server.fetch(
            messages, ['RFC822']
        ).items():
            body = message_data[b'RFC822']
            email_message = email.message_from_bytes(
                body, policy=email.policy.default)
            user = extract_info_from_email(email_message)
            read_email_message(email_message, user)

        if delete:
            server.delete_messages(messages)

    else:
        logger.info(
            f"IMAP import: Failed to login to imap server {imap_server}."
            " Please double check IMAP account credentials."
        )
