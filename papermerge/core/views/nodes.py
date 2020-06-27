import json
import logging

from django.http import (
    HttpResponse,
    HttpResponseBadRequest
)
from django.contrib.auth.decorators import login_required
from papermerge.core.models import BaseTreeNode


logger = logging.getLogger(__name__)


@login_required
def browse(request, parent_id=None):

    if parent_id.strip() == '':
        parent_id = None

    nodes = BaseTreeNode.objects.filter(parent_id=parent_id)

    return HttpResponse(
        json.dumps(
            {
                'nodes': [node.to_dict() for node in nodes],
                'parent_id': parent_id
            }
        ),
        content_type="application/json"
    )


@login_required
def nodeinfo(request, node_id):
    try:
        node = BaseTreeNode.objects.get(id=node_id)
    except BaseTreeNode.DoesNotExist:
        return HttpResponseBadRequest(
            json.dumps({
                'node': node.to_dict()
            }),
            content_type="application/json"
        )

    return HttpResponse(
        json.dumps({
            'node': node.to_dict()
        }),
        content_type="application/json"
    )

