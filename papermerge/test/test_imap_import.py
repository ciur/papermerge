import os
from email.message import EmailMessage
import email

from django.test import TestCase, override_settings

from .utils import (
    create_root_user,
    create_margaret_user,
    create_elizabet_user
)

from papermerge.core.importers.imap import extract_info_from_email, read_email_message
from papermerge.core.models import Document

BASE_DIR = os.path.dirname(__file__)


def create_email(
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
    if not attachment:
        return msg.as_bytes()
    with open(attachment, 'rb') as fp:
        attachment = fp.read()
    msg.add_attachment(attachment, maintype=maintype, subtype=subtype)
    return msg.as_bytes()


class TestIMAPImporterByUser(TestCase):
    def setUp(self):
        self.user = create_root_user()
        self.margaret = create_margaret_user()
        self.elizabet = create_elizabet_user()

    @override_settings(PAPERMERGE_IMPORT_MAIL_BY_USER=True)
    def test_extract_user_by_mail_address_not_allowed_user(self):
        body = create_email(user=self.margaret)
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        user = extract_info_from_email(email_message)
        self.assertIsNone(user)

    @override_settings(PAPERMERGE_IMPORT_MAIL_BY_USER=True)
    def test_extract_user_by_mail_address_allowed_user(self):
        body = create_email(user=self.elizabet)
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        self.elizabet.mail_by_user = True
        self.elizabet.save()
        user = extract_info_from_email(email_message)
        self.assertNotEqual(user, self.margaret)
        self.assertEqual(user, self.elizabet)

    def test_extract_user_by_mail_address_not_allowed_settings(self):
        body = create_email(user=self.margaret)
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        user = extract_info_from_email(email_message)
        self.assertIsNone(user)

    def test_extract_user_by_mail_address_allowed_settings(self):
        body = create_email(user=self.elizabet)
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        self.elizabet.mail_by_user = True
        self.elizabet.save()
        user = extract_info_from_email(email_message)
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

    @override_settings(PAPERMERGE_IMPORT_MAIL_BY_SECRET=True)
    def test_extract_user_by_secret_not_allowed_user(self):
        body = create_email(subject='SECRET{this-is-margaret-secret}')
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        user = extract_info_from_email(email_message)
        self.assertIsNone(user)

    @override_settings(PAPERMERGE_IMPORT_MAIL_BY_SECRET=True)
    def test_extract_user_by_secret_allowed_user(self):
        body = create_email(subject='SECRET{this-is-elizabet-secret}')
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        self.elizabet.mail_by_secret = True
        self.elizabet.save()
        user = extract_info_from_email(email_message)
        self.assertNotEqual(user, self.margaret)
        self.assertEqual(user, self.elizabet)

    def test_extract_user_by_secret_not_allowed_settings(self):
        body = create_email(subject='SECRET{this-is-margaret-secret}')
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        user = extract_info_from_email(email_message)
        self.assertIsNone(user, self.margaret)

    def test_extract_user_by_secret_allowed_settings(self):
        body = create_email(subject='SECRET{this-is-elizabet-secret}')
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        self.elizabet.mail_by_secret = True
        self.elizabet.save()
        user = extract_info_from_email(email_message)
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
        body = create_email(
            attachment=file_path,
            maintype='application',
            subtype='pdf',
        )
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        user = extract_info_from_email(email_message)
        self.assertIsNone(user)
        read_email_message(email_message, user, skip_ocr=True)
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
        body = create_email(
            attachment=file_path,
            maintype='image',
            subtype='jpg',
        )
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        user = extract_info_from_email(email_message)
        self.assertIsNone(user)
        read_email_message(email_message, user, skip_ocr=True)
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
        body = create_email(
            attachment=file_path,
            maintype='application',
            subtype='x-tar',
        )
        email_message = email.message_from_bytes(
            body, policy=email.policy.default)
        user = extract_info_from_email(email_message)
        self.assertIsNone(user)
        read_email_message(email_message, user, skip_ocr=True)
        self.assertEqual(
            Document.objects.count(),
            0
        )
