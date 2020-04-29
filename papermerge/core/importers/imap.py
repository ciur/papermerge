import ssl
import email
import tempfile
from django.conf import settings
from imapclient import IMAPClient
from papermerge.core.document_importer import DocumentImporter


def read_email_message(message):
    """
    message is an instance of python's module email.message
    """
    imported_count = 0

    for part in message.walk():
        # search for payload
        maintype = part.get_content_maintype()
        subtype = part.get_content_subtype()
        if maintype == 'application' and subtype == 'pdf':

            with tempfile.NamedTemporaryFile() as temp:
                temp.write(part.get_payload(decode=True))
                temp.flush()
                DocumentImporter(temp.name, filename=part.get_filename)

    return imported_count


def import_attachment():

    imported_count = 0

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    IMAP_SERVER = 
    USERNAME = 
    PASSWORD = 

    with IMAPClient(
        config['imap_server'],
        ssl_context=ssl_context
    ) as server:
        server.login(config['username'], config['password'])
        server.select_folder('INBOX')
        messages = server.search(['UNSEEN'])

        logger.debug(
            f"IMAP UNSEEN messages {len(messages)}"
            f" for {config['username']}"
        )

        for uid, message_data in server.fetch(
            messages, 'RFC822'
        ).items():
            email_message = email.message_from_bytes(
                message_data[b'RFC822']
            )
            imported_count = read_email_message(email_message)
