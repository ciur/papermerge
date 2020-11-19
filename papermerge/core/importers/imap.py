import ssl
import email
import tempfile
import logging
from django.conf import settings
from imapclient import IMAPClient
from imapclient.exceptions import LoginError

from papermerge.core.document_importer import DocumentImporter

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


def read_email_message(message):
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
                imp = DocumentImporter(temp.name)
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

        for uid, message_data in server.fetch(
            messages, 'RFC822'
        ).items():
            email_message = email.message_from_bytes(
                message_data[b'RFC822']
            )
            read_email_message(email_message)
    else:
        logger.info(
            f"IMAP import: Failed to login to imap server {imap_server}."
            " Please double check IMAP account credentials."
        )
