import logging

from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from papermerge.core.auth import create_access
from papermerge.core.models import Access, Diff, Document, Folder
from papermerge.core.storage import default_storage
from papermerge.core.tasks import normalize_pages

from .metadata_plugins import apply_metadata_plugins
from .signal_definitions import page_hocr_ready

logger = logging.getLogger(__name__)


@receiver(page_hocr_ready, sender="worker")
def handle_metadata_plusgins(sender, **kwargs):
    document_id = kwargs.get('document_id', False)
    page_num = kwargs.get('page_num', False)

    apply_metadata_plugins(
        document_id=document_id,
        page_num=page_num
    )


@receiver(post_delete, sender=Document)
def update_user_storage(sender, instance, **kwargs):
    # update user storage size
    user = instance.user
    user.update_current_storage()


@receiver(post_save, sender=Document)
def update_user_storage_after_doc_creation(sender, instance, **kwargs):
    # update user storage size
    user = instance.user
    user.update_current_storage()


@receiver(pre_delete, sender=Document)
def deleteFiles(sender, instance, **kwargs):
    """
    Will delete associated physical (pdf) file.

    More exactly it will delete whatever it is inside
    associated folder in which original file was saved
    (e.g. all preview images).

    Preview images as well all other associated files
    are irreversibly deleted.
    """
    logger.debug("Deleting files for doc_id={} of user_id={}".format(
        instance.id,
        instance.user.id
    ))

    default_storage.delete_doc(
        instance.path
    )


def node_post_save(sender, node, created, *kwargs):
    if created:
        # New node instance was created.
        # Create associated Access Model:
        # node creater has full access.
        create_access(
            node=node,
            model_type=Access.MODEL_USER,
            name=node.user.username,
            access_type=Access.ALLOW,
            access_inherited=False,
            permissions=Access.OWNER_PERMS_MAP  # full access
        )

    # Consider this two persons use case:
    # User uploader uploads scans for user margaret.
    # Initially document is in uploader's Inbox folder.
    # Afterwards, uploader moves new document X into common shared_folder.
    # shared_folder has full access permissions for
    # boths uploader and margaret.
    # When margaret sees document X, she copies it into
    # her private folder X_margaret_fld. X_margaret_fld is
    # owned only by margaret.
    # Now document X's path is margaret//X_margaret_fld/X.pdf
    # If X.pdf access permissions stay same, then uploader will
    # still have access to X.pdf (via search) which means,
    # that margaret will need to change manually X.pdf's
    # access permissions. To avoid manual change of access
    # permissions from margaret side - papermerge feature
    # is that X.pdf inherits access permissions from new
    # parent (X_margaret_fld). Thus, just by copying it,
    # X.pdf becomes margaret private doc - and uploader
    # lose its access to it.
    if node.parent:  # current node has a parent?
        # Following statement covers case when node
        # is moved from one parent to another parent.

        # When node moved from one parent to another
        # it get all its access replaced by access list of the
        # parent
        access_diff = Diff(
            operation=Diff.REPLACE,
            instances_set=node.parent.access_set.all()
        )
        node.propagate_changes(
            diffs_set=[access_diff],
            apply_to_self=True
        )
    else:
        # In case node has no parent, all its access permission
        # remain the same.
        pass


@receiver(post_save, sender=Folder)
def save_node_folder(sender, instance, created, **kwargs):
    node_post_save(sender, instance, created, kwargs)


@receiver(post_save, sender=Document)
def save_node_doc(sender, instance, created, **kwargs):
    node_post_save(sender, instance, created, kwargs)


@receiver(post_save, sender=Document)
def inherit_metadata_keys(sender, instance, created, **kwargs):
    """
    When moved into new folder, documents will inherit their parent
    metadata keys
    """
    # if doc has a parent
    if instance.parent:
        instance.inherit_kv_from(instance.parent)
        for page in instance.pages.all():
            page.inherit_kv_from(instance.parent)


@receiver(post_save, sender=Folder)
def inherit_metadata_keys_from_parent(sender, instance, created, **kwargs):
    """
    When created or moved folders will inherit metadata keys from their
    parent.
    """
    # if folder was just created and has a parent
    if created and instance.parent:
        instance.inherit_kv_from(instance.parent)


@receiver(post_save, sender=Document)
def normalize_pages_from_doc_handler(sender, instance, created, **kwargs):
    """Update async this document pages' attributes page.norm_*
    """
    logger.debug("Post save doc => normalize_pages")
    normalize_pages(origin=instance)


@receiver(post_save, sender=Folder)
def normalize_pages_from_folder_handler(sender, instance, created, **kwargs):
    """Update async folder pages attributes page.norm_*
    """
    normalize_pages(origin=instance)
