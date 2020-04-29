import ssl
import email
import tempfile
import logging
from django.conf import settings
from imapclient import IMAPClient
from papermerge.core.document_importer import DocumentImporter

logger = logging.getLogger(__name__)


def read_email_message(message):
    """
    message is an instance of python's module email.message
    """
    for part in message.walk():
        # search for payload
        maintype = part.get_content_maintype()
        subtype = part.get_content_subtype()
        if maintype == 'application' and subtype == 'pdf':

            with tempfile.NamedTemporaryFile() as temp:
                temp.write(part.get_payload(decode=True))
                temp.flush()
                imp = DocumentImporter(temp.name)
                imp.import_file(
                    delete_after_import=False
                )


def import_attachment():

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    imap_server = settings.PAPERMERGE_IMPORT_MAIL_HOST
    username = settings.PAPERMERGE_IMPORT_MAIL_USER
    password = settings.PAPERMERGE_IMPORT_MAIL_PASS

    with IMAPClient(
        imap_server,
        ssl_context=ssl_context
    ) as server:
        server.login(username, password)
        server.select_folder('INBOX')
        messages = server.search(['UNSEEN'])

        logger.debug(
            f"IMAP UNSEEN messages {len(messages)}"
            f" for {username}"
        )

        for uid, message_data in server.fetch(
            messages, 'RFC822'
        ).items():
            email_message = email.message_from_bytes(
                message_data[b'RFC822']
            )
            read_email_message(email_message)

