import io
import json
import os
from pathlib import Path
import tarfile

from django.test import TestCase

from papermerge.core.models import Document, Folder
from papermerge.core.storage import default_storage
from papermerge.test.utils import create_root_user
from papermerge.core.backup_restore import (
    backup_documents,
    _can_restore,
    restore_documents
)

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestBackupRestore(TestCase):

    def setUp(self) -> None:
        self.testcase_user = create_root_user()

    def test_backup_single_document(self):
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

        with io.BytesIO() as memoryfile:
            backup_documents(memoryfile, self.testcase_user)
            memoryfile.seek(0)

            self.assertTrue(
                _can_restore(memoryfile),
                'generated backup.tar is not valid'
            )
            memoryfile.seek(0)

            backup_file = tarfile.open(fileobj=memoryfile, mode='r')
            backup_json = backup_file.extractfile('backup.json')
            backup_info = json.loads(backup_json.read())

            self.assertIsNotNone(
                backup_info.get('documents'),
                'backup.json did not have a key "documents"'
            )
            self.assertIs(
                len(backup_info.get('documents')), 1,
                'backup.json key documents had more or less than one entry'
            )
            self.assertIs(
                len(backup_file.getnames()),
                2,
                'backup.tar had more or less than 2 entries'
            )
            self.assertTrue(
                'berlin.pdf' in backup_file.getnames(),
                'berlin.pdf was not in the backup.tar'
            )

    def test_backup_document_hierachy(self):
        folder_1 = Folder.objects.create(
            title='1',
            parent=None,
            user=self.testcase_user
        )
        folder_2 = Folder.objects.create(
            title='2',
            parent=folder_1,
            user=self.testcase_user
        )
        folder_3 = Folder.objects.create(
            title='3',
            parent=folder_1,
            user=self.testcase_user
        )
        Folder.objects.create(
            title='4',
            parent=None,
            user=self.testcase_user
        )

        document_path = os.path.join(
            BASE_DIR, "data", "berlin.pdf"
        )

        doc_1 = Document.create_document(
            user=self.testcase_user,
            title='berlin.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            file_name='berlin.pdf',
            parent_id=folder_2.id,
            page_count=3
        )

        default_storage.copy_doc(
            src=document_path,
            dst=doc_1.path.url(),
        )

        doc_2 = Document.create_document(
            user=self.testcase_user,
            title='berlin.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            file_name='berlin.pdf',
            parent_id=folder_3.id,
            page_count=3
        )

        default_storage.copy_doc(
            src=document_path,
            dst=doc_2.path.url(),
        )

        with io.BytesIO() as memoryfile:
            backup_documents(memoryfile, self.testcase_user)
            memoryfile.seek(0)

            self.assertTrue(
                _can_restore(memoryfile),
                'generated backup.tar is not valid'
            )
            memoryfile.seek(0)

            backup_file = tarfile.open(fileobj=memoryfile, mode='r')
            backup_json = backup_file.extractfile('backup.json')
            backup_info = json.loads(backup_json.read())

            self.assertIsNotNone(
                backup_info.get('documents'),
                'backup.json did not have a key "documents"'
            )
            self.assertIs(
                len(backup_info.get('documents')), 2,
                'backup.json key documents had more or less than two entry'
            )
            self.assertIs(
                len(backup_file.getnames()),
                3,
                'backup.tar had more or less than 2 entries'
            )
            self.assertTrue(
                '1/2/berlin.pdf' in backup_file.getnames(),
                'berlin.pdf was not in the backup.tar at folder 1/2/'
            )
            self.assertTrue(
                '1/3/berlin.pdf' in backup_file.getnames(),
                'berlin.pdf was not in the backup.tar at folder 1/3/'
            )
            self.assertFalse(
                '4' in backup_file.getnames(),
                'Folder 4 was in backup.tar but should have been ignored'
            )

    def test_restore_backup(self):
        restore_path = os.path.join(
            BASE_DIR, "data", "testdata.tar"
        )

        with open(restore_path, 'rb') as restore_archive:
            restore_documents(restore_archive, self.testcase_user.username)

        folder_1 = Folder.objects.filter(title='1', parent=None).first()
        self.assertIsNotNone(folder_1, 'Folder "1" was not restored')

        folder_2 = Folder.objects.filter(title='2', parent=None).first()
        self.assertIsNotNone(folder_2, 'Folder "2" was not restored')

        folder_3 = Folder.objects.filter(title='3', parent=folder_2).first()
        self.assertIsNotNone(folder_3, 'Folder "3" was not restored')

        document_berlin_1 = Document.objects.filter(
            title='berlin.pdf',
            parent=folder_1
        ).first()
        self.assertIsNotNone(
            document_berlin_1,
            'Document "berlin.pdf" in folder 1 was not restored'
        )

        document_berlin_3 = Document.objects.filter(
            title='berlin.pdf',
            parent=folder_3
        ).first()

        self.assertIsNotNone(
            document_berlin_3,
            'Document "berlin.pdf" in folder 3 was not restored'
        )

    def test_restore_backup_documents_in_root(self):
        """
        In case tar file contain documents in root (i.e. documents not
        part any folder) - restore_documents function should not throw
        an error (e.g. AttributeError: 'NoneType' object has no attribute 'id')
        """
        restore_path = os.path.join(
            BASE_DIR, "data", "one-doc-in-root-testdata.tar"
        )

        with open(restore_path, 'rb') as restore_archive:
            # should not throw an exception
            restore_documents(restore_archive, self.testcase_user.username)
