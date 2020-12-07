from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

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


class NodeAuthBackend:
    """
    In this context Object = Node = papermerge.core.models.BaseTreeNode

    Each object has many access model associated. Access model is either
    assigned directly to the node (object) or inherited via object's parent.
    Inheritance of access models happens during node creation or via user's
    management of access instances. In other words when deciding if user
    has permission for a node - node's parents are not consulted.

    Each Access model has one access type associated (ALLOW or DENY) and
    either one group or user, access model basically says:
        allow (or deny) access to this user (or group) using given permission
        set.

    In case there are multiple access instances with same permission but with
    different access_type (elizabeth is both allowed and denied read
    permission on node X) then deny access type has priority (elizabeth will
    be denied access to node X).
    """

    def authenticate(self, request, username=None, password=None):
        # mandatory interface for django auth backend.
        # But we don't use it.
        return None

    def get_user(self, user_id):
        # mandatory interface for django auth backend.
        # But we don't use it.
        return None

    def django_get_user_permissions(self, user_obj):
        return user_obj.role.permissions.all()

    def django_get_group_permissions(self, user_obj):
        user_groups_field = get_user_model()._meta.get_field('groups')
        user_groups_query = 'group__%s' % user_groups_field.related_query_name()  # noqa

        return Permission.objects.filter(**{user_groups_query: user_obj})

    def django_get_all_permissions(self, user_obj):
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = {
                *self.django_get_permissions(user_obj, 'user'),
                *self.django_get_permissions(user_obj, 'group'),
            }

        return user_obj._perm_cache

    def django_get_permissions(self, user_obj, from_name):

        perm_cache_name = '_%s_perm_cache' % from_name
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = getattr(
                    self, 'django_get_%s_permissions' % from_name
                )(user_obj)
            perms = perms.values_list(
                'content_type__app_label', 'codename'
            ).order_by()
            setattr(
                user_obj,
                perm_cache_name,
                {"%s.%s" % (ct, name) for ct, name in perms}
            )
        return getattr(user_obj, perm_cache_name)

    def _django_has_perm(self, user_obj, perm):
        """
        Gets user permissions from associated role.
        """
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()

        if user_obj.is_superuser:
            perms = Permission.objects.all()
        else:
            # this is the only major difference from django's
            # own implementation: it gets permissions from associated role
            if not user_obj.role:
                # if non superuser does not have associated a role
                # he/she basically is has no permissios at all!
                return set()
            perms = user_obj.role.permissions.all()

        # By returning permissions this way - will be able to
        # reuse ``user_obj.has_perm(...)`` method.
        _perms = perms.values_list(
            'content_type__app_label',
            'codename'
        ).order_by()

        __perms = {"%s.%s" % (ct, name) for ct, name in _perms}

        return perm in __perms

    def get_perms_dict(self, user_obj, obj_list, perms):
        """
        Returns a dictionary. Each key of the dictionary
        # is the id of the node. Value of the key is permissions
        # dictionary

        Input:

        user_obj = user instance core.models.User
        obj_list = a list of instances of type core.models.node.BaseTreeNode
        perms = a list of permissions e.g. ['read', 'write', delete]

        Output:

            a dictionary with given perms as keys. Example:

            ret = user.get_perms_dict([n1, n2], ['read', 'write', 'delete'])
            ret = {
                n1.id: {
                    'read': True,
                    'delete': False,
                    'write': False
                },
                n2.id: {
                    'read': False,
                    'delete': False,
                    'write': False
                }
            }
        """
        ret = {}
        deny_perms = self._get_all_deny_permissions(
            user_obj,
            obj_list
        )

        allow_perms = self._get_all_allow_permissions(
            user_obj,
            obj_list
        )

        for obj_id in allow_perms.keys():
            ret[obj_id] = {}
            for perm in allow_perms[obj_id]:
                ret[obj_id][perm] = True

        for obj_id in deny_perms.keys():
            for perm in deny_perms[obj_id]:
                # 'deny' permissions overwrite 'allow'
                ret[obj_id][perm] = False

        return ret

    def has_perm(self, user_obj, perm, obj=None):
        """
        Main function. However it is optional in django auth backend.
        verifies if user has permissions to access a given file or folder
        via papermerge.core.models.Access models.
        """
        # Access.DENY has priority over Access.ALLOW
        if not obj:
            return self._django_has_perm(user_obj, perm)

        deny_perms = self._get_all_deny_permissions(user_obj, obj)
        allow_perms = self._get_all_allow_permissions(user_obj, obj)

        if perm in deny_perms:
            return False

        return perm in allow_perms

    def _get_group_permissions(self, user_obj, obj_or_list, access_type):
        if not isinstance(obj_or_list, models.Model):
            if len(obj_or_list) == 0:
                return set()
        else:
            if not obj_or_list:
                return {}

        if not isinstance(obj_or_list, models.Model):
            ret = {}
            obj_ids = [obj.id for obj in obj_or_list]
            all_access_items = Access.objects.prefetch_related(
                'permissions'
            ).filter(
                access_type=access_type
            ).filter(
                node_id__in=obj_ids
            )
            for access in all_access_items:
                if not access.group:
                    continue

                if user_obj.groups.filter(name=access.group.name).exists():
                    ret[access.node_id] = {
                        perm.codename for perm in access.permissions.all()
                    }

            return ret

        # else -> case when obj_or_list is a single object

        for access in obj_or_list.access_set.filter(access_type=access_type):
            if not access.group:
                continue

            if user_obj.groups.filter(name=access.group.name).exists():
                return {perm.codename for perm in access.permissions.all()}

        return set()

    def _get_user_permissions(self, user_obj, obj_or_list, access_type):
        if not isinstance(obj_or_list, models.Model):
            if len(obj_or_list) == 0:
                return set()
        else:
            if not obj_or_list:
                return {}

        if not isinstance(obj_or_list, models.Model):
            ret = {}
            obj_ids = [obj.id for obj in obj_or_list]
            all_access_items = Access.objects.prefetch_related(
                'permissions'
            ).filter(
                access_type=access_type
            ).filter(
                node_id__in=obj_ids
            )

            for access in all_access_items:
                if access.user == user_obj:
                    ret[access.node_id] = {
                        perm.codename for perm in access.permissions.all()
                    }

            return ret

        # else -> case when obj_or_list is a single object

        for access in obj_or_list.access_set.filter(access_type=access_type):
            if access.user == user_obj:
                return {perm.codename for perm in access.permissions.all()}

        return set()

    def _get_all_allow_permissions(self, user_obj, obj_or_list):
        """
        Returns a set of permissions (python set())
        """
        all_user_perms = self._get_user_permissions(
            user_obj, obj_or_list, Access.ALLOW
        )
        all_group_perms = self._get_group_permissions(
            user_obj, obj_or_list, Access.ALLOW
        )

        ret = {}

        if not isinstance(obj_or_list, models.Model):
            for obj in obj_or_list:
                ret[obj.id] = {
                    *all_user_perms.get(obj.id, set()),
                    *all_group_perms.get(obj.id, set()),
                }
            return ret

        return {
            *all_user_perms, *all_group_perms
        }

    def _get_all_deny_permissions(self, user_obj, obj_or_list):
        """
        Returns a set of permissions (python set())
        """
        all_user_perms = self._get_user_permissions(
            user_obj,
            obj_or_list,
            Access.DENY
        )
        all_group_perms = self._get_group_permissions(
            user_obj,
            obj_or_list,
            Access.DENY
        )

        ret = {}

        if isinstance(obj_or_list, models.Model):
            return {
                *all_user_perms,
                *all_group_perms,
            }

        for obj in obj_or_list:
            ret[obj.id] = {
                *all_user_perms.get(obj.id, set()),
                *all_group_perms.get(obj.id, set()),
            }

        return ret
