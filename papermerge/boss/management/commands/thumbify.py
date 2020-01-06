import logging
import os
import sys
from shutil import copyfile
from django.conf import settings
from django.core.management.base import BaseCommand
from papermerge.core.models import Document
from papermerge.core.lib.preview import DocumentFile
from papermerge.core.utils import get_media_root

try:
    from django_tenants.utils import get_tenant_model
except:
    get_tenant_model = None

from django.db import connection

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """
    Generate MEDIA directory with as symbolic links to single jpeg/pdf file.
    Used in staging environment. Instead of copying/mounting
    whole MEDIA directory,
    just run this script. Suddenly 100 GB production media becomes 1 MB :)
    (all media files are just symbolic links to thumbidy.pdf and thumbidy.jpeg)
"""

    def thumbify(self, tenant_name, src_thumb_path):
        all_docs = Document.objects.all()

        for doc in all_docs:
            df = DocumentFile(
                fmtdirstr="user_{}/document_{}".format(doc.user.id, doc.id),
                file_name=doc.file_name,
                media_root=get_media_root()
            )
            if not df.exists:
                # create all dirs (symlink parents)
                os.makedirs(
                    os.path.dirname(df.abspath)
                )
                # create symlink itself
                os.symlink(
                    src_thumb_path,
                    df.abspath
                )

    def cloud_handle(self, src_thumb_path):
        TenantModel = get_tenant_model()
        for tenant in TenantModel.objects.all():
            # TODO: hmmm, I don't like this 'public' exception.
            # From PostgreSQL public schema is not special in any way,
            # why shoult it be from djante-tenants point of view?
            # I think this is a bug.
            if tenant.name == 'public':
                continue  # wtf? fix me.

            connection.set_tenant(tenant)
            self.thumbify(
                tenant_name=tenant.name,
                src_thumb_path=src_thumb_path
            )

    def onprem_handle(self):
        self.thumbify(tenant_name=None)

    def install_thumb(self):
        # copy from thumbify/thumb.pdf to MEDIA_ROOT
        src_thumb_path = os.path.join(
            os.path.dirname(__file__),
            "thumbify",
            "thumb.pdf"
        )
        dst_thumb_path = os.path.join(
            settings.MEDIA_ROOT,
            "thumb.pdf"
        )
        if not os.path.exists(src_thumb_path):
            print("Thumb file {} was not found".format(src_thumb_path))
            sys.exit(1)

        copyfile(
            src_thumb_path,
            dst_thumb_path
        )

        return dst_thumb_path

    def handle(self, *args, **options):
        src_thumb_path = self.install_thumb()
        if get_tenant_model:
            self.cloud_handle(src_thumb_path)
        else:
            self.onprem_handle()
