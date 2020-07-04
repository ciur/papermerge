import json
import logging

from django.http import (
    HttpResponse,
    HttpResponseBadRequest
)
from django.contrib.auth.decorators import login_required
from papermerge.core.models import BaseTreeNode
from django.urls import reverse


logger = logging.getLogger(__name__)


@login_required
def browse_view(request, parent_id=None):

    nodes = BaseTreeNode.objects.filter(parent_id=parent_id)
    nodes_list = []

    for node in nodes:

        node_dict = node.to_dict()

        if node.is_document():
            node_dict['img_src'] = reverse(
                'core:preview',
                args=(node.id, 4, 1)
            )
            node_dict['document_url'] = reverse(
                'core:document',
                args=(node.id,)
            )

        nodes_list.append(node_dict)

    return HttpResponse(
        json.dumps(
            {
                'nodes': nodes_list,
                'parent_id': parent_id
            }
        ),
        content_type="application/json"
    )


@login_required
def breadcrumb_view(parent, parent_id=None):

    nodes = []

    node = None
    try:
        node = BaseTreeNode.objects.get(id=parent_id)
    except BaseTreeNode.DoesNotExist:
        pass

    if node:
        nodes = [
            item.to_dict() for item in node.get_ancestors(include_self=True)
        ]

    return HttpResponse(
        json.dumps({
            'nodes': nodes,
        }),
        content_type="application/json"
    )


@login_required
def node_view(request, node_id):
    try:
        node = BaseTreeNode.objects.get(id=node_id)
    except BaseTreeNode.DoesNotExist:
        return HttpResponseBadRequest(
            json.dumps({
                'node': node.to_dict()
            }),
            content_type="application/json"
        )

    if request.method == "DELETE":

        node.delete()

        return HttpResponse(
            json.dumps({
                'msg': 'OK'
            }),
            content_type="application/json"
        )

    return HttpResponse(
        json.dumps({
            'node': node.to_dict()
        }),
        content_type="application/json"
    )


@login_required
def nodes_view(request):
    if request.method == "POST":

        data = json.loads(request.body)
        node_ids = [item['id'] for item in data]
        BaseTreeNode.objects.filter(id__in=node_ids).delete()

        return HttpResponse(
            json.dumps({
                'msg': 'OK'
            }),
            content_type="application/json"
        )

    return HttpResponse(
        json.dumps({
            'msg': 'OK'
        }),
        content_type="application/json"
    )
