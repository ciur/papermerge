import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden
)
from django.utils.translation import gettext as _

from papermerge.core.models import Access, BaseTreeNode
from .decorators import json_response

logger = logging.getLogger(__name__)


@json_response
@login_required
def tags_view(request, node_id):
    try:
        node = BaseTreeNode.objects.get(id=node_id)
    except BaseTreeNode.DoesNotExist:
        msg = _("Node does not exist")
        return msg, HttpResponseBadRequest.status_code

    if request.user.has_perm(Access.PERM_WRITE, node):
        data = json.loads(request.body)
        tags = [item['name'] for item in data['tags']]
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
