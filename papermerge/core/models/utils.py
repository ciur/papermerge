import inspect
import logging

from django.apps import apps

from .node import BaseTreeNode


logger = logging.getLogger(__name__)


def recursive_delete(queryset_or_node_instance):
    """
    Given a queryset of nodes (BaseTreeNode instance),
    traverse recursively (depth traversal) and delete
    all nodes starting from leaf nodes upwards.

    In theory this function is redundant as node.delete() should
    take care of whole subtree.

    But because of a nasty bug -
        see papermerge.test.test_node.TestRecursiveDelete
    it is a necessary workaround
    """
    if isinstance(queryset_or_node_instance, BaseTreeNode):
        queryset = BaseTreeNode.objects.filter(
            id=queryset_or_node_instance.id
        )
    else:
        queryset = queryset_or_node_instance

    for node in queryset:

        descendants = node.get_descendants()
        if descendants.count() > 0:
            recursive_delete(descendants)

        # At this point all descendants were deleted.
        # Self delete :)
        try:
            node.delete()
        except BaseTreeNode.DoesNotExist:
            # this node was deleted by earlier recursive call
            # it is ok, just sktip
            pass


def get_fields(model):
    """
    Returns django fields of current ``model``.

    Does not include inherited fields.
    """
    return model._meta.get_fields(include_parents=False)


def group_per_model(models, **kwargs):
    """
    groups kwargs per model
    """
    ret = {}

    for model in models:
        fields = get_fields(model)
        for field in fields:
            if field.name in kwargs.keys():
                ret.setdefault(model, {}).update(
                    {field.name: kwargs[field.name]}
                )

    return ret
