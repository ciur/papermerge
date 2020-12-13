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
    restore_documents,
    build_tar_archive
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
        doc = Document.objects.create_document(
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
            dst=doc.path().url(),
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
                f"berlin.pdf__{doc.id}" in backup_file.getnames(),
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

        doc_1 = Document.objects.create_document(
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
            dst=doc_1.path().url(),
        )

        doc_2 = Document.objects.create_document(
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
            dst=doc_2.path().url(),
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
                f"1/2/berlin.pdf__{doc_1.id}" in backup_file.getnames(),
                'berlin.pdf was not in the backup.tar at folder 1/2/'
            )
            self.assertTrue(
                f"1/3/berlin.pdf__{doc_2.id}" in backup_file.getnames(),
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
            restore_documents(restore_archive, self.testcase_user)

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
            restore_documents(restore_archive, self.testcase_user)


class TestBuildTarArchive(TestCase):
    """
    Test functionality which builds downloaded tar archive with
    selected nodes (documents and folders)
    """

    def setUp(self):
        self.testcase_user = create_root_user()

    def test_basic(self):
        """
        Creates following hierarchy:

            + Accounting
            +   Expenses
            +       berlin_ex_1.pdf
            +       berlin_ex_2.pdf
            + berlin_root_1.pdf
            + berlin_root_2.pdf
        """
        acc = Folder.objects.create(
            title='Accounting',
            parent=None,
            user=self.testcase_user
        )
        ex = Folder.objects.create(
            title='Expenses',
            parent=acc,
            user=self.testcase_user
        )

        document_path = os.path.join(
            BASE_DIR, "data", "berlin.pdf"
        )

        doc_in_root_1 = Document.objects.create_document(
            user=self.testcase_user,
            title='berlin_root_1.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            file_name='berlin_root_1.pdf',
            page_count=3
        )
        default_storage.copy_doc(
            src=document_path,
            dst=doc_in_root_1.path().url(),
        )

        doc_in_root_2 = Document.objects.create_document(
            user=self.testcase_user,
            title='berlin_root_2.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            file_name='berlin_root_2.pdf',
            page_count=3
        )
        default_storage.copy_doc(
            src=document_path,
            dst=doc_in_root_2.path().url(),
        )

        doc_in_ex_1 = Document.objects.create_document(
            user=self.testcase_user,
            title='berlin_ex_1.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            parent_id=ex.id,
            file_name='berlin_ex_1.pdf',
            page_count=3
        )
        default_storage.copy_doc(
            src=document_path,
            dst=doc_in_ex_1.path().url(),
        )

        doc_in_ex_2 = Document.objects.create_document(
            user=self.testcase_user,
            title='berlin_ex_2.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            parent_id=ex.id,
            file_name='berlin_ex_2.pdf',
            page_count=3
        )
        default_storage.copy_doc(
            src=document_path,
            dst=doc_in_ex_2.path().url(),
        )

        """
        User selected two documents in the root dir berlin_root_1.pdf,
        and berlin_root_1.pdf and the Accounting folder.
        Selection is marked with square brackets [...]

            + [Accounting]
            +   Expenses
            +       berlin_ex_1.pdf
            +       berlin_ex_2.pdf
            + [berlin_root_1.pdf]
            + [berlin_root_2.pdf]
        """
        selected_ids = [
            doc_in_root_1.id, doc_in_root_2.id, acc.id
        ]

        with io.BytesIO() as memoryfile:
            build_tar_archive(  # <-- THIS IS WHAT WE ARE TESTING
                fileobj=memoryfile,
                node_ids=selected_ids
            )
            memoryfile.seek(0)
            archive_file = tarfile.open(fileobj=memoryfile, mode='r')
            berlin_root_1_handle = archive_file.extractfile(
                'berlin_root_1.pdf'
            )
            data = berlin_root_1_handle.read()
            self.assertTrue(len(data) > 0)

            berlin_ex_1_handle = archive_file.extractfile(
                'Accounting/Expenses/berlin_ex_1.pdf'
            )
            data = berlin_ex_1_handle.read()
            self.assertTrue(len(data) > 0)

            with self.assertRaises(KeyError):
                # there is no file Accounting/Expenses/Paris.pdf
                # in archive, thus, KeyError exception is expected
                archive_file.extractfile(
                    'Accounting/Expenses/Paris.pdf'
                )

    def test_basic_two_folders(self):
        """
        Creates following hierarchy:

            + Folder_1
            +   berlin_f_1.pdf
            + Folder_2
            +   berlin_f_2.pdf
            + berlin_root_1.pdf
            + berlin_root_2.pdf
        """
        f1 = Folder.objects.create(
            title='Folder_1',
            parent=None,
            user=self.testcase_user
        )
        f2 = Folder.objects.create(
            title='Folder_2',
            parent=None,
            user=self.testcase_user
        )

        document_path = os.path.join(
            BASE_DIR, "data", "berlin.pdf"
        )

        doc_in_root_1 = Document.objects.create_document(
            user=self.testcase_user,
            title='berlin_root_1.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            file_name='berlin_root_1.pdf',
            page_count=3
        )
        default_storage.copy_doc(
            src=document_path,
            dst=doc_in_root_1.path().url(),
        )

        doc_in_root_2 = Document.objects.create_document(
            user=self.testcase_user,
            title='berlin_root_2.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            file_name='berlin_root_2.pdf',
            page_count=3
        )
        default_storage.copy_doc(
            src=document_path,
            dst=doc_in_root_2.path().url(),
        )

        doc_in_f_1 = Document.objects.create_document(
            user=self.testcase_user,
            title='berlin_f_1.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            parent_id=f1.id,
            file_name='berlin_f_1.pdf',
            page_count=3
        )
        default_storage.copy_doc(
            src=document_path,
            dst=doc_in_f_1.path().url(),
        )

        doc_in_f_2 = Document.objects.create_document(
            user=self.testcase_user,
            title='berlin_f_2.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            parent_id=f2.id,
            file_name='berlin_f_2.pdf',
            page_count=3
        )
        default_storage.copy_doc(
            src=document_path,
            dst=doc_in_f_2.path().url(),
        )

        """
        User selected two documents in the root dir berlin_root_1.pdf,
        and berlin_root_1.pdf plus Folder_1 and Folder_2.
        Selection is marked with square brackets [...]

            + [Folder_1]
            +   berlin_f_1.pdf
            + [Folder_2]
            +   berlin_f_2.pdf
            + [berlin_root_1.pdf]
            + [berlin_root_2.pdf]
        """
        selected_ids = [
            doc_in_root_1.id, doc_in_root_2.id, f1.id, f2.id
        ]

        with io.BytesIO() as memoryfile:
            build_tar_archive(  # <-- THIS IS WHAT WE ARE TESTING
                fileobj=memoryfile,
                node_ids=selected_ids
            )
            memoryfile.seek(0)
            archive_file = tarfile.open(fileobj=memoryfile, mode='r')
            berlin_root_1_handle = archive_file.extractfile(
                'berlin_root_1.pdf'
            )
            data = berlin_root_1_handle.read()
            self.assertTrue(len(data) > 0)

            berlin_f_1_handle = archive_file.extractfile(
                'Folder_1/berlin_f_1.pdf'
            )
            data = berlin_f_1_handle.read()
            self.assertTrue(len(data) > 0)

            berlin_f_2_handle = archive_file.extractfile(
                'Folder_2/berlin_f_2.pdf'
            )
            data = berlin_f_2_handle.read()
            self.assertTrue(len(data) > 0)

            with self.assertRaises(KeyError):
                # there is no file Accounting/Expenses/Paris.pdf
                # in archive, thus, KeyError exception is expected
                archive_file.extractfile(
                    'Accounting/Expenses/Paris.pdf'
                )
