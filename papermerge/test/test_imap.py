from django.test import TestCase

from papermerge.core.importers.imap import is_payload_supported

class TestImapImporter(TestCase):

    def test_is_payload_supported(self):
        # supported i.e. this mime type is
        # an attachment of a supported document type.
        self.assertTrue(
            is_payload_supported("application", "pdf")
        )
        self.assertTrue(
            is_payload_supported("application", "PDF")
        )
        self.assertTrue(
            is_payload_supported("image", "png")
        )
        self.assertTrue(
            is_payload_supported("image", "jpeg")
        )
        self.assertTrue(
            is_payload_supported("image", "jpg")
        )
        self.assertTrue(
            is_payload_supported("image", "TIFF")
        )
        self.assertTrue(
            is_payload_supported("application", "octet-stream")
        )

        # not supported
        self.assertFalse(
            is_payload_supported("application", "vnd.oasis.opendocument.text")
        )
        self.assertFalse(
            is_payload_supported("application", "plain")
        )
        self.assertFalse(
            is_payload_supported("text", "html")
        )
        self.assertFalse(
            is_payload_supported("multipart", "mixed")
        )
        # Invalid input
        self.assertFalse(
            is_payload_supported("multipart", None)
        )
        self.assertFalse(
            is_payload_supported("", "text")
        )
        self.assertFalse(
            is_payload_supported(None, None)
        )







