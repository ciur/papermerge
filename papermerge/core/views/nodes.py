import json
import logging

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden
)
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404

from papermerge.core.models import BaseTreeNode, Access, Folder
from papermerge.core.models.utils import recursive_delete

logger = logging.getLogger(__name__)


@login_required
def browse_view(request, parent_id=None):

    nodes = BaseTreeNode.objects.filter(parent_id=parent_id).exclude(
        title=Folder.INBOX_NAME
    )
    nodes_list = []
    parent_kv = []

    if parent_id:

        parent_node = get_object_or_404(
            BaseTreeNode, id=parent_id
        )

        for item in parent_node.kv.all():
            parent_kv.append(item.to_dict())

    # Will returns a dictionary. Each key of the dictionary
    # is the id of the node. Value of the key is permissions
    # dictionary e.g.
    # {
    #   '23': {"read": True, "delete": False },
    #   '24': {"read": True, "delete": False },
    #   '25': {"read": False, "delete": False }
    # }
    nodes_perms = request.user.get_perms_dict(
        nodes, Access.ALL_PERMS
    )

    for node in nodes:
        if nodes_perms[node.id].get(Access.PERM_READ, False):
            node_dict = node.to_dict()
            # and send user_perms to the frontend client

            node_dict['user_perms'] = nodes_perms[node.id]

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
                'parent_id': parent_id,
                'parent_kv': parent_kv
            }
        ),
        content_type="application/json"
    )


@login_required
def breadcrumb_view(request, parent_id=None):

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
def node_by_title_view(request, title):
    """
    Useful in case of special folders like inbox (and trash in future).
    Returns node id, children_count, title of specified node's title.
    Title specified is insensitive (i.e. INBOX = Inbox = inbox).
    """
    node = get_object_or_404(
        BaseTreeNode,
        title__iexact=title
    )

    return HttpResponse(
        json.dumps({
            'id': node.id,
            'title': node.title,
            'children_count': node.get_children().count(),
            'url': reverse('node_by_title', args=('inbox',))
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
        if request.user.has_perm(Access.PERM_DELETE, node):
            node.delete()
        else:
            msg = f"{request.user.username} does not have" +\
                f" permission to delete {node.title}"
            return HttpResponseForbidden(
                json.dumps({
                    'msg': msg
                }),
                content_type="application/json"
            )

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

        queryset = BaseTreeNode.objects.filter(id__in=node_ids)
        for node in queryset:
            # is used allowd to delete ?
            if not request.user.has_perm(Access.PERM_DELETE, node):
                # if user does not have delete permission on
                # one node - forbid entire operation!
                msg = f"{request.user.username} does not have" +\
                    f" permission to delete {node.title}"
                return HttpResponseForbidden(
                    json.dumps({
                        'msg': msg
                    }),
                    content_type="application/json"
                )
        # yes, user is allowed to delete all nodes,
        # proceed with delete opration
        recursive_delete(queryset)

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
