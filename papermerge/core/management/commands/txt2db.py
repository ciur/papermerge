import logging
from django.core.management.base import BaseCommand
from papermerge.core.models import Document

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Read .txt files and insert its content
    into associated DB column.

    It will update text field of all associated pages first
    (from .txt files) and then concatinate all text field into
    doc.text field.
"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--document-id',
            '-d',
            help="Limit update only for specified document_id"
        )

    def update_field(
        self,
        document_id=False
    ):
        docs = []
        ocred_count = 0

        if document_id:
            docs = Document.objects.filter(
                basetreenode_ptr_id=document_id
            )
        else:
            docs = Document.objects.all()

        for doc in docs:
            if doc.update_text_field():
                ocred_count += 1

    def onprem_handle(self):
        self.update_field(tenant_name=None)

    def handle(self, *args, **options):
        document_id = options.get(
            'document_id',
            False
        )
        self.update_field(
            document_id=document_id
        )
