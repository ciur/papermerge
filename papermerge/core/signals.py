import logging

from django.db.models.signals import (
    pre_delete,
    post_delete,
    post_save,
)
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from allauth.account.signals import (
    email_confirmed,
    user_logged_in,
    user_logged_out,
    password_changed,
    password_reset
)

from papermerge.core.models import (
    Folder,
    Document,
    Access,
    AccessDiff
)
from papermerge.core.auth import (
    create_access
)
from papermerge.core.storage import default_storage
from papermerge.core.utils import get_tenant_name


User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Document)
def update_user_storage(sender, instance, **kwargs):
    # update user storage size
    user = User.objects.get(id=instance.user.id)
    user.update_current_storage()


@receiver(post_save, sender=Document)
def update_user_storage_after_doc_creation(sender, instance, **kwargs):
    # update user storage size
    user = User.objects.get(id=instance.user.id)
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
    logger.info("Deleting files for doc_id={} of user_id={}".format(
        instance.id,
        instance.user.id
    ))

    default_storage.delete_document(
        instance.path
    )


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    logger.debug(f"user_logged_in {user.username}")


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    logger.debug(f"user_logged_out {user.username}")


@receiver(password_changed)
def password_changed_handler(sender, request, user, **kwargs):
    logger.info(f"password_changed {user.username}")


@receiver(password_reset)
def password_reset_handler(sender, request, user, **kwargs):
    logger.info(f"password_reset {user.username}")


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):

    user = User.objects.get(email=email_address.email)
    vml_access = Permission.objects.get(codename='vml_access')
    vml_root = Permission.objects.get(codename='vml_root')
    user.user_permissions.add(vml_access)
    user.user_permissions.add(vml_root)
    user.is_active = True
    user.save()

    logger.info(
        f"registration_log mail confirmed"
        f" company={get_tenant_name()}"
        f" username={user.username}"
        f" email={email_address.email}"
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
        access_diff = AccessDiff(
            operation=AccessDiff.REPLACE,
            access_set=node.parent.access_set.all()
        )
        node.propagate_access_changes(
            access_diffs=[access_diff],
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

