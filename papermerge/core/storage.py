import os
import boto3


from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible
from django.core.files import File
from django.conf import settings
from django.utils._os import safe_join
from django.utils.encoding import filepath_to_uri
from six.moves.urllib.parse import urljoin

from papermerge.core import models

from pmworker.endpoint import (
    get_bucketname,
    get_keyname
)


@deconstructible
class DocumentStorage(FileSystemStorage):
    """
    """
    def path(self, name):
        """
        At the beginnig, all pdf's were stored in MEDIA_ROOT.
        However, later, I moved each file xyz.pdf into
        MEDIA_ROOT/xyz/ folder. This is why, before returning
        path of file, I check if it is new or old format.
        Basically, if method is because of migration.
        """
        dirname, filename = os.path.split(name)
        if not dirname:
            root, ext = os.path.splitext(name)
            dirname = str(root)
            return safe_join(self.location, dirname, name)
        else:
            return safe_join(self.location, name)

    def _open(self, name, mode='rb'):
        return File(open(self.path(name), mode))

    def url(self, name):

        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")

        url = filepath_to_uri(name)

        if url is not None:
            url = url.lstrip('/')

        root, _ = os.path.splitext(os.path.basename(name))
        return urljoin(self.base_url, "{}/{}".format(root, url))


def is_storage_left(filepath, user=False):
    """
        Storage space is associated per tenant. However,
        it is computed as per user profile.
        If user=False, then user considered is root user.

        This user profile thingy is there because in future versions
        there will be space quote allocation per user; and per user
        quoate will be derived from tenant quota (i.e root user).
    """
    max_storage = settings.MAX_STORAGE_SIZE
    file_size = os.path.getsize(filepath)
    if not user:
        user = models.get_root_user()
    profile = user.userprofile
    new_storage_size = file_size + profile.current_storage_size

    if new_storage_size > max_storage * 1024:
        return False

    return True


def remove_file(doc_url):
    """
    Will remove actually the directory associated with that user
    """
    s3 = boto3.resource('s3')
    bucketname = get_bucketname(doc_url)
    keyname = get_keyname(doc_url)

    bucket = s3.Bucket(bucketname)
    bucket.Object(keyname).delete()
