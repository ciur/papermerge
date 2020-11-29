import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden
)
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

from papermerge.core import validators
from papermerge.core.models import Access, BaseTreeNode, Tag
from .decorators import json_response

logger = logging.getLogger(__name__)


@json_response
@login_required
def tags_view(request, node_id):
    """
    Add/remove tags per single node
    """
    try:
        node = BaseTreeNode.objects.get(id=node_id)
    except BaseTreeNode.DoesNotExist:
        msg = _("Node does not exist")
        return msg, HttpResponseBadRequest.status_code

    if request.user.has_perm(Access.PERM_WRITE, node):
        data = json.loads(request.body)
        tags = [item['name'] for item in data['tags']]
        try:
            # validate user's input
            for tag in tags:
                validators.safe_character_validator(tag)
        except ValidationError as e:
            return e.message, HttpResponseBadRequest.status_code

        node.tags.set(
            *tags,
            tag_kwargs={"user": request.user}
        )
    else:
        msg = _(
            "%(username)s does not have "
            "write permission on node %(title)s"
        ) % {
            'username': request.user.username,
            'title': node.title
        }

        return msg, HttpResponseForbidden.status_code

    return 'OK'


@json_response
@login_required
def nodes_tags_view(request):
    """
    Add/remove tags per bulk of nodes.

    Example of valid input:
        {"tags":[{"name":"test"}],"nodes":[92,52]}

    There must be at least one node, otherwise
    HttpReponseBadRequest will be returned.
    Tags however, can be empty. In case of empty tag list -
    all given nodes will be "stripped" from all tags - sort
    of bulk remove.
    """
    data = json.loads(request.body)
    node_ids = data.get('nodes', [])
    tags = data.get('tags', [])

    if not node_ids:
        msg = _("No nodes provided")
        return msg, HttpResponseBadRequest.status_code

    tags = [item['name'] for item in tags]

    nodes = BaseTreeNode.objects.filter(id__in=node_ids)

    nodes_perms = request.user.get_perms_dict(
        nodes, Access.ALL_PERMS
    )

    for node in nodes:
        if nodes_perms[node.id].get(Access.PERM_WRITE, False):
            try:
                # validate user's input
                for tag in tags:
                    validators.safe_character_validator(tag)
            except ValidationError as e:
                return e.message, HttpResponseBadRequest.status_code

            node.tags.set(
                *tags,
                tag_kwargs={"user": request.user}
            )
        else:
            msg = _(
                "%(username)s does not have "
                "write permission on node %(title)s"
            ) % {
                'username': request.user.username,
                'title': node.title
            }

            return msg, HttpResponseForbidden.status_code

    return 'OK'


@json_response
@login_required
def alltags_view(request):

    all_tags = [
        {'name': tag.name}
        for tag in Tag.objects.filter(user=request.user)
    ]

    return {'tags': all_tags}
