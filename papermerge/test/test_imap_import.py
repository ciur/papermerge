import os
from email.message import EmailMessage
import email

from django.test import TestCase

from .utils import (
    create_root_user,
    create_margaret_user,
    create_elizabet_user
)

from papermerge.core.importers.imap import (
    get_matching_user,
    trigger_document_pipeline
)
from papermerge.core.models import Document

BASE_DIR = os.path.dirname(__file__)


class TestIMAPImporterByUser(TestCase):

    def setUp(self):
        self.user = create_root_user()
        self.margaret = create_margaret_user()
        self.elizabet = create_elizabet_user()

    def test_extract_user_by_mail_address_not_allowed_user(self):

        email_message = _create_email(user=self.margaret)

        user = get_matching_user(
            email_message,
            by_user=True
        )

        self.assertIsNone(user)

    def test_extract_user_by_mail_address_allowed_user(self):

        email_message = _create_email(user=self.elizabet)

        self.elizabet.mail_by_user = True
        self.elizabet.save()

        user = get_matching_user(
            email_message,
            by_user=True
        )

        self.assertNotEqual(user, self.margaret)
        self.assertEqual(user, self.elizabet)

    def test_extract_user_by_mail_address_not_allowed_settings(self):

        email_message = _create_email(user=self.margaret)

        user = get_matching_user(email_message)
        self.assertIsNone(user)

    def test_extract_user_by_mail_address_allowed_settings(self):

        email_message = _create_email(user=self.elizabet)

        self.elizabet.mail_by_user = True
        self.elizabet.save()
        user = get_matching_user(email_message)
        self.assertIsNone(user)


class TestIMAPImporterBySecret(TestCase):

    def setUp(self):

        self.user = create_root_user()
        self.margaret = create_margaret_user()
        self.elizabet = create_elizabet_user()
        self.margaret.mail_secret = 'this-is-margaret-secret'
        self.margaret.save()
        self.elizabet.mail_secret = 'this-is-elizabet-secret'
        self.elizabet.save()

    def test_extract_user_by_secret_not_allowed_user(self):

        email_message = _create_email(
            subject='SECRET{this-is-margaret-secret}'
        )

        user = get_matching_user(
            email_message,
            by_secret=True
        )

        self.assertIsNone(user)

    def test_extract_user_by_secret_allowed_user(self):

        email_message = _create_email(
            subject='SECRET{this-is-elizabet-secret}'
        )

        self.elizabet.mail_by_secret = True
        self.elizabet.save()

        user = get_matching_user(
            email_message,
            by_secret=True
        )

        self.assertNotEqual(user, self.margaret)
        self.assertEqual(user, self.elizabet)

    def test_extract_user_by_secret_not_allowed_settings(self):

        email_message = _create_email(
            subject='SECRET{this-is-margaret-secret}'
        )

        user = get_matching_user(email_message)
        self.assertIsNone(user, self.margaret)

    def test_extract_user_by_secret_allowed_settings(self):

        email_message = _create_email(
            subject='SECRET{this-is-elizabet-secret}'
        )

        self.elizabet.mail_by_secret = True
        self.elizabet.save()
        user = get_matching_user(email_message)
        self.assertIsNone(user)


class TestIMAPImporterIngestion(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_pdf_imap_importer(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "berlin.pdf"
        )
        email_message = _create_email(
            attachment=file_path,
            maintype='application',
            subtype='pdf',
        )

        user = get_matching_user(email_message)
        self.assertIsNone(user)
        trigger_document_pipeline(email_message, user, skip_ocr=True)
        self.assertEqual(
            Document.objects.count(),
            1
        )

    def test_jpg_imap_importer(self):

        file_path = os.path.join(
            BASE_DIR,
            "data",
            "page-1.jpg"
        )
        email_message = _create_email(
            attachment=file_path,
            maintype='image',
            subtype='jpg',
        )

        user = get_matching_user(email_message)
        self.assertIsNone(user)
        trigger_document_pipeline(email_message, user, skip_ocr=True)
        self.assertEqual(
            Document.objects.count(),
            1
        )

    def test_tar_imap_importer(self):

        file_path = os.path.join(
            BASE_DIR,
            "data",
            "testdata.tar"
        )
        email_message = _create_email(
            attachment=file_path,
            maintype='application',
            subtype='x-tar',
        )

        user = get_matching_user(email_message)
        self.assertIsNone(user)
        trigger_document_pipeline(email_message, user, skip_ocr=True)

        self.assertEqual(
            Document.objects.count(),
            0
        )


def _create_email(
    attachment=None,
    maintype=None,
    subtype=None,
    user=None,
    subject='This is a test email'
):
    msg = EmailMessage()

    msg['To'] = 'papermerge@example.com'

    if user:
        email_address = user.email
    else:
        email_address = 'user@example.com'

    msg['From'] = email_address
    msg['Subject'] = subject

    if attachment:
        with open(attachment, 'rb') as fp:
            attachment = fp.read()

        msg.add_attachment(attachment, maintype=maintype, subtype=subtype)

    email_message = email.message_from_bytes(
        msg.as_bytes(),
        policy=email.policy.default
    )

    return email_message

