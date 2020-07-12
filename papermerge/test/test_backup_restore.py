import io
import json
import os
from pathlib import Path
import tarfile

from django.test import TestCase

from papermerge.core.models import Document
from papermerge.core.storage import default_storage
from papermerge.test.utils import create_root_user
from papermerge.core.backup_restore import backup_documents, _can_restore

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestBackupRestore(TestCase):
    def setUp(self) -> None:
        self.testcase_user = create_root_user()

    def test_single_document(self):

        document_path = os.path.join(
            BASE_DIR, "data", "berlin.pdf"
        )
        doc = Document.create_document(
            user=self.testcase_user,
            title='berlin.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            file_name='berlin.pdf',
            parent_id=None,
            page_count=3
        )

        default_storage.copy_doc(
            src=document_path,
            dst=doc.path.url(),
        )

        # Check if document is created
        new_document = Document.objects.filter(title='berlin.pdf').first()
        self.assertIsNotNone(new_document)

        with io.BytesIO() as memoryfile:
            backup_documents(memoryfile)
            memoryfile.seek(0)

            self.assertTrue(_can_restore(memoryfile), 'generated backup.tar is not valid')
            memoryfile.seek(0)

            backup_file = tarfile.open(fileobj=memoryfile, mode='r')
            backup_json = backup_file.extractfile('backup.json')
            backup_info = json.loads(backup_json.read())

            self.assertIsNotNone(backup_info.get('documents'), 'backup.json did not have a key "documents"')
            self.assertIs(len(backup_info.get('documents')),1, 'backup.json key documents had more or less than one entry')
            self.assertIs(len(backup_file.getnames()), 2, 'backup.tar had more or less than 2 entries')
            self.assertTrue('berlin.pdf' in backup_file.getnames(), 'berlin.pdf was not in the backup.tar')




