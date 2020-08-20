from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Access(models.Model):
    # Access model guards files and folder i.e. decision
    # if a user has or hasn't permission to perform any operation
    # on give node (file/folder) is made only in respect to associated
    # access models.
    #
    # Every node (file or folder) has many access entries.
    # Every access has either one group
    # or one user associated. If a node has exactly one user
    # and one group associated - there will be two access models
    # created - one for user and one for group.

    PERM_READ = "read"
    PERM_WRITE = "write"
    PERM_DELETE = "delete"
    PERM_CHANGE_PERM = "change_perm"
    PERM_TAKE_OWNERSHIP = "take_ownership"

    ALL_PERMS = [
        PERM_READ,
        PERM_WRITE,
        PERM_DELETE,
        PERM_CHANGE_PERM,
        PERM_TAKE_OWNERSHIP
    ]

    ALLOW = "allow"
    DENY = "deny"
    MODEL_USER = "user"
    MODEL_GROUP = "group"
    OWNER_PERMS_MAP = {
        PERM_READ: True,
        PERM_WRITE: True,
        PERM_DELETE: True,
        PERM_CHANGE_PERM: True,
        PERM_TAKE_OWNERSHIP: True
    }

    node = models.ForeignKey(
        'BaseTreeNode',
        models.CASCADE,
    )
    access_type = models.CharField(
        max_length=16,
        choices=[
            (ALLOW, _('Allow')),
            (DENY, _('Deny')),
        ],
        default='allow',
    )
    # inherited access is read only
    access_inherited = models.BooleanField(
        default=False
    )
    group = models.ForeignKey(
        Group,
        verbose_name=_('group'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'User',
        verbose_name=_('user'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    permissions = models.ManyToManyField(
        Permission
    )

    def create(node, access_inherited, access):
        if access.user:
            new_access = Access.objects.create(
                user=access.user,
                access_type=access.access_type,
                node=node,
                access_inherited=access_inherited
            )
        elif access.group:
            new_access = Access.objects.create(
                group=access.group,
                access_type=access.access_type,
                node=node,
                access_inherited=access_inherited
            )
        else:
            raise ValueError(
                "Access object must have associated either user or group"
            )

        new_access.permissions.add(
            *access.permissions.all()
        )

        return new_access

    def perms_codenames(self):
        return {p.codename for p in self.permissions.all()}

    def __str__(self):
        #perms = [
        #    p.codename for p in self.permissions.all()
        #]
        #perms = 'PPP'
        name = '-'
        if self.user:
            name = f"User({self.user.username})"
        elif self.group:
            name = f"Group({self.group.name})"

        typ = self.access_type

        return f"Access({name}, {typ}, ...)"

    class Meta:
        permissions = [
            ("read", "Read Access"),
            ("write", "Write Access"),
            ("delete", "Delete Access"),
            ("change_perm", "Change Permissions Access"),
            ("take_ownership", "Take Ownership Access"),
        ]

    def __hash__(self):

        name = ''

        if self.user:
            name = f"User({self.user.username})"
        elif self.group:
            name = f"Group({self.group.name})"

        typ = self.access_type
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        return hash((name, typ))

    def __eq__(self, access):
        """
        Two access models are equal if all conditions
        are true:
        * accesses are attached to the some node
        * have same access type (allow or deny)
        * have both either same user or same group

        NOTE: inheritance flag does not matter.
        """
        if self.node.id != access.node.id:
            return False

        if self.user and access.user:
            return self.user == access.user

        if self.group and access.group:
            return self.group == access.group

        return False

    def has_perm(self, codename):
        return self.permissions.filter(
            codename=codename
        ).count() > 0

    def extract_perm_dict(self):
        result = {
            Access.PERM_READ: False,
            Access.PERM_WRITE: False,
            Access.PERM_DELETE: False,
            Access.PERM_CHANGE_PERM: False,
            Access.PERM_TAKE_OWNERSHIP: False
        }
        for perm in self.permissions.all():
            result[perm.codename] = True

        return result

    def perm_diff(self, compare_with):
        """
        passed compare with can be either:
        * a dictionary {'read': true, 'delete': false} etc
        * another Access model instance
        """
        perm_dict1 = self.extract_perm_dict()

        if isinstance(compare_with, Access):
            perm_dict2 = compare_with.extract_perm_dict()

        if isinstance(compare_with, dict):
            perm_dict2 = compare_with

        return perm_dict1 != perm_dict2

    def set_perms(self, perm_hash):

        content_type = ContentType.objects.get(
            app_label="core",
            model="access",
        )
        codenames = [
            key for key, value in perm_hash.items() if perm_hash[key]
        ]
        perms = Permission.objects.filter(
            codename__in=codenames,
            content_type=content_type
        )
        self.permissions.clear()
        if perms.count() > 0:
            self.permissions.add(*perms)

    def update_from(self, access):
        if self != access:
            return False

        self.access_type = access.access_type
        self.permissions.clear()
        self.permissions.set(
            access.permissions.all()
        )
