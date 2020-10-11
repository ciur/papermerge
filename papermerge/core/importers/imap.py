import ssl
import email
import tempfile
import logging
from django.conf import settings
from imapclient import IMAPClient
from imapclient.exceptions import LoginError
from imapclient.response_types import BodyData

from papermerge.core.document_importer import DocumentImporter

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


def is_payload_supported(maintype: str, subtype: str) -> bool:
    """
    Papermerge supports pdf, tiff, jpeg and png formats.
    Returns true if mimetype (maintype + subtype) is one of
    supported types:

    PDF => maintype=application, subtype=pdf
    TIFF => maintype=image, subtype=tiff
    Jpeg => maintype=image, subtype=jpeg
    png => maintype=image, subtype=png
    Also will return true in case of 'application/octet-stream'.
    """
    if not maintype:
        return False

    if not subtype:
        return False

    duo = (maintype.lower(), subtype.lower())

    supported = (
        ('application', 'octet-stream'),
        ('application', 'pdf'),
        ('image', 'png'),
        ('image', 'jpeg'),
        ('image', 'jpg'),
        ('image', 'tiff'),
    )

    if duo in supported:
        return True

    return False


def read_email_message(message, user=None):
    """
    message is an instance of python's module email.message
    """
    for index, part in enumerate(message.walk()):
        # search for payload
        maintype = part.get_content_maintype()
        subtype = part.get_content_subtype()
        logger.debug(
            f"IMAP import: payload {index} maintype={maintype}"
            f" subtype={subtype}."
        )
        if is_payload_supported(maintype=maintype, subtype=subtype):
            logger.debug(
                "IMAP import: importing..."
            )
            with tempfile.NamedTemporaryFile() as temp:
                temp.write(part.get_payload(decode=True))
                temp.flush()
                imp = DocumentImporter(temp.name, user_object=user)
                imp.import_file(
                    delete_after_import=False
                )
        else:
            logger.debug(
                "IMAP import: ignoring payload."
            )


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
        server.select_folder('INBOX')
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
            sender_address = '{}@{}'.format(sender.mailbox.decode(), sender.host.decode())
            try:
                message_secret = body.split(b'SECRET{')[1].split(b'}')[0]
            except IndexError:
                message_secret = None
            email_message = email.message_from_bytes(
                body
            )

            # Priority to sender address
            if by_user:
                user = User.objects.filter(
                        email=sender_address
                        ).first()
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

            # Otherwise put it into superuser's inbox
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
