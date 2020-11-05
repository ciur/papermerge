from django.db import models
from django.core.exceptions import PermissionDenied

from papermerge.core.models import AbstractNode


class Policy(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    # policy dictates if specific document
    # may be deleted.
    allow_delete = models.BooleanField(
        default=False
    )

    def __str__(self):

        n = self.name
        d = self.allow_delete

        return f"Policy({n}, allow_delete={d})"


class Node(AbstractNode):
    """
    All nodes may have one retention
    policy associated
    """
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name='states',
        blank=True,
        null=True
    )

    def delete(self):
        """
        raise Permission denied if policy
        does not allow delection.
        """
        if not self.policy:
            super().delete()
            return (1, {type(self): 1})

        # if there is a policy associated
        # which denies permission
        if not self.policy.allow_delete:
            raise PermissionDenied()

        super().delete()
        return (1, {type(self): 1})

    def __repr__(self):
        _i = self.id
        _p = self.policy
        _b = self.base_ptr

        return f"NodePart(id={_i}, policy={_p}, base_ptr={_b})"


class NodeX(AbstractNode):
    policy_x = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name='statesx',  # Note: 'x'
        blank=True,
        null=True
    )

    def delete(self):
        if not self.policy_x:
            super().delete()
            return (1, {type(self): 1})

        # silently object deletion
        if not self.policy_x.allow_delete:
            # returning 0 as first item in tuple
            # will silently prevent document deletion
            return (0, {type(self): 0})

        super().delete()
        return (1, {type(self): 1})

    def __repr__(self):
        _i = self.id
        _p = self.policy
        _b = self.base_ptr

        return f"NodeXPart(id={_i}, policy={_p}, base_ptr={_b})"
