from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from papermerge.core.models import Access, Diff

# custom user is used - papermerge.core.models.User
User = get_user_model()


def delete_access_perms(node, access_list):
    """
    same input as for set_access_perms
    """

    access_diff_d = Diff(operation=Diff.DELETE)
    # by the user
    for access_item in node.access_set.all():
        if access_item.user:
            name = access_item.user.username
            model_type = 'user'
        elif access_item.group:
            name = access_item.group.name
            model_type = 'group'

        # if node's access list contains items
        # which are in access_list - delete respective
        # node's access
        filtered = [
            x for x in access_list
            if x['model'] == model_type and x['name'] == name
        ]

        if len(filtered) > 0:
            # further propagation is done via pre_delete
            # signals for Access models
            access_diff_d.add(access_item)
            access_item.delete()

    return [access_diff_d]


def set_access_perms(node, access_list):
    """
    node is an instance of core.models.BaseTreeNode
    access is an array/list of hashes of following
    format:

    access = [
        {
            'model': 'user',
            'access_type': 'allow',
            'name': 'margaret',
            'permissions': {
                'read': true,
                'write': true,
                'delete': true,
                'change_perm': true,
                'take_ownership': true
            }
        },
        {
            'model': 'group',
            'access_type': 'allow',
            'name': 'employee',
            'permissions': {
                'read': true,
                'write': true,
                'delete': true,
                'change_perm': true,
                'take_ownership': true
            }
        }, ...
    ]
    """
    # first, add new access entries to the node
    # or update existing onces.
    access_diff_u = Diff(operation=Diff.UPDATE)
    access_diff_a = Diff(operation=Diff.ADD)

    for access_hash in access_list:
        access = get_access_for(
            node=node,
            model_type=access_hash['model'],
            name=access_hash['name']
        )
        if access:
            if access.perm_diff(access_hash['permissions']):
                access.set_perms(access_hash['permissions'])
                access_diff_u.add(access)
        else:
            access = create_access(
                node=node,
                model_type=access_hash['model'],
                name=access_hash['name'],
                access_type=access_hash['access_type'],
                access_inherited=False,
                permissions=access_hash['permissions']
            )
            access_diff_a.add(access)

    ret = []
    if len(access_diff_a) > 0:
        ret.append(access_diff_a)

    if len(access_diff_u) > 0:
        ret.append(access_diff_u)

    return ret


def create_access(
    node,
    model_type,
    access_type,
    name,
    permissions,
    access_inherited
):
    """
    permissions is a dictionary of following format:

        {
            'read': True|False,
            'delete': True|False,
            'write': True|False,
            'take_ownership': True|False,
            'change_perm': True|False,
        }
    """
    content_type, _ = ContentType.objects.get_or_create(
        app_label="core",
        model="access",
    )
    # if key is either missing in permissions dictionary
    # (is not one of 5 permissions) or will have False value
    # permission wont be set.
    perm_keys = [  # permissions keys to set
        key for key, value in permissions.items() if value
    ]

    if len(perm_keys) == 0:
        raise Exception(
            "auth.create_access: I refuse to create access with "
            "empty permissions."
        )

    perms = Permission.objects.filter(
        codename__in=perm_keys,
        content_type=content_type
    )

    if perms.count() == 0 and len(perm_keys) > 0:
        raise Exception(
            f"Not a single of Core Access Permissions was "
            f"found: {perm_keys}."
        )

    if model_type == 'user':
        user = User.objects.get(username=name)
        access = Access.objects.create(
            user=user,
            access_type=access_type,
            node=node,
            access_inherited=access_inherited
        )
    elif model_type == 'group':
        group = Group.objects.get(name=name)
        access = Access.objects.create(
            group=group,
            access_type=access_type,
            node=node
        )

    access.permissions.add(*perms)

    return access


def get_access_perms_as_hash(
    node,
    model_type,
    name
):
    """
        node = core.models.BaseTreeNode instance
        model_type = 'user' or 'group' as string
        name = username in case of user, and name
            in case of group model type
    """
    access = get_access_for(node, model_type, name)

    if not access:
        return {}

    result = {}
    result[Access.PERM_READ] = access.has_perm(Access.PERM_READ)
    result[Access.PERM_WRITE] = access.has_perm(Access.PERM_WRITE)
    result[Access.PERM_DELETE] = access.has_perm(Access.PERM_DELETE)
    result[Access.PERM_CHANGE_PERM] = access.has_perm(Access.PERM_CHANGE_PERM)
    result[Access.PERM_TAKE_OWNERSHIP] = access.has_perm(
        Access.PERM_TAKE_OWNERSHIP
    )

    return result


def create_access_perms():
    """
    Permissions related to the Access model.
    Access model grants permissions to BaseTreeNodes.
    """
    results = []
    # make sure description here matches the one
    # of the papermerge.core.models.Access.Meta.permissions
    # i.e. Change Permissions Access, etc
    permissions = (
        (Access.PERM_CHANGE_PERM, "Change Permissions Access"),
        (Access.PERM_TAKE_OWNERSHIP, "Take Ownership Access"),
        (Access.PERM_READ, "Read Access"),
        (Access.PERM_WRITE, "Write Access"),
        (Access.PERM_DELETE, "Delete Access"),
    )
    content_type, _ = ContentType.objects.get_or_create(
        app_label="core",
        model="access",
    )
    for perm in permissions:
        p, dummy = Permission.objects.get_or_create(
            codename=perm[0],
            name=perm[1],
            content_type=content_type
        )
        dummy = dummy
        results.append(p)

    return results


def get_access_for(node, model_type, name):

    access = None

    if model_type == Access.MODEL_USER:
        access = Access.objects.filter(
            node=node,
            user__username=name
        ).first()
    elif model_type == Access.MODEL_GROUP:
        access = Access.objects.filter(
            node=node,
            group__name=name
        ).first()

    return access
