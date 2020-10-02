from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from papermerge.core.models import Access


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
        return user_obj.user_permissions.all()

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
        Permissions not related to node access (django way)
        """
        permissions = self.django_get_all_permissions(user_obj)
        return perm in permissions

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
