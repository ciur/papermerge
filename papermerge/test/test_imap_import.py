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

        email_message = _create_email(
            from_field=self.margaret.email
        )

        user = get_matching_user(
            email_message,
            by_user=True
        )

        self.assertIsNone(user)

    def test_extract_user_by_mail_address_allowed_user(self):

        email_message = _create_email(
            from_field=self.elizabet.email
        )

        self.elizabet.mail_by_user = True
        self.elizabet.save()

        user = get_matching_user(
            email_message,
            by_user=True
        )

        self.assertNotEqual(user, self.margaret)
        self.assertEqual(user, self.elizabet)

    def test_extract_user_by_mail_address_not_allowed_settings(self):

        email_message = _create_email(from_field=self.margaret.email)

        user = get_matching_user(email_message)
        self.assertIsNone(user)

    def test_extract_user_by_mail_address_allowed_settings(self):

        email_message = _create_email(from_field=self.elizabet.email)

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

    def test_match_user_by_secret_in_subject_1(self):
        """
        Email secret can be placed in email subject
        """
        email_message = _create_email(
            # notice that secret is in message subject
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

    def test_match_user_by_secret_in_subject_2(self):
        """
        Email secret can be placed in email subject AND
        there can be white spaces AROUND the secret
        """
        email_message = _create_email(
            # notice that secret is in message subject
            # and is there are white spaces around the
            # secret message. However, there are
            # no spaces between word SECRET and immediately following
            # it opening curly bracket
            subject='SECRET{    this-is-elizabet-secret }'
        )

        self.elizabet.mail_by_secret = True
        self.elizabet.save()

        user = get_matching_user(
            email_message,
            by_secret=True
        )

        self.assertNotEqual(user, self.margaret)
        self.assertEqual(user, self.elizabet)

    def test_match_user_by_secret_in_body_1(self):
        """
        If email secret is detected in email body AND
        user.mail_by_secret == True, then ``get_matching_user``
        should return correct user.
        """

        email_message = _create_email(
            # notice that secret is in the message body
            body='hello ! SECRET{this-is-elizabet-secret} Bye bye!'
        )

        # Both margaret AND elizabeth have mail_by_secret
        # attribute set to True.
        self.margaret.mail_by_secret = True
        self.margaret.save()

        self.elizabet.mail_by_secret = True
        self.elizabet.save()

        user = get_matching_user(
            email_message,
            by_secret=True
        )
        self.assertNotEqual(user, self.margaret)
        self.assertEqual(user, self.elizabet)

    def test_match_user_by_secret_in_body_2(self):
        """
        If email secret is detected in email body BUT
        relevant user do not have user.mail_by_secret set to True,
        then ``get_matching_user`` should return None
        """

        email_message = _create_email(
            # notice that secret is in message body
            body='SECRET{this-is-margaret-secret}'
        )
        # Both margaret AND elizabeth have mail_by_secret
        # attribute set to False (!)
        self.margaret.mail_by_secret = False  # !important
        self.margaret.save()

        self.elizabet.mail_by_secret = False  # !important
        self.elizabet.save()

        user = get_matching_user(email_message)
        self.assertIsNone(user, self.margaret)

    def test_match_user_by_secret_in_body_plus_whitespaces(self):
        """
        secret is placed in the message body.

            SECRET{ ... }

        Notice that between secret message and curly bracket there can
        be whitespaces; however between keyword SECRET and immediately
        following opening curly bracket - there is no space.
        """

        email_message = _create_email(
            # notice that secret is in the message body
            body="""
            Lieber Freund,

            Blah, blah, blah und es gib ein White Space da!

                SECRET{     this-is-elizabet-secret  }

            PS:
                no space is allowed between keyword SECRET and
                immediately following curly bracket.
            """
        )

        # Both margaret AND elizabeth have mail_by_secret
        # attribute set to True.
        self.margaret.mail_by_secret = True
        self.margaret.save()

        self.elizabet.mail_by_secret = True
        self.elizabet.save()

        user = get_matching_user(
            email_message,
            by_secret=True
        )

        self.assertNotEqual(user, self.margaret)
        self.assertEqual(user, self.elizabet)

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
    to_field="to_user@test1.com",
    from_field="from_user@test2.com",
    subject="This is a test email",
    body="Almost empty text message",
    attachment=None,
    maintype=None,
    subtype=None,
):
    """
    Builds and returns an ``email.message.EmailMessage`` instance
    with to, from, subject, body and eventually an
    attachment in the email body.
    """
    msg = EmailMessage()

    msg['To'] = to_field
    msg['From'] = from_field
    msg['Subject'] = subject
    msg.set_content(body)

    if attachment:
        with open(attachment, 'rb') as fp:
            attachment = fp.read()

        msg.add_attachment(attachment, maintype=maintype, subtype=subtype)

    email_message = email.message_from_bytes(
        msg.as_bytes(),
        policy=email.policy.default
    )

    return email_message
