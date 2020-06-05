import json
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from papermerge.core.auth import (delete_access_perms,
                                  get_access_perms_as_hash, set_access_perms)
from papermerge.core.models import Access, BaseTreeNode, User

logger = logging.getLogger(__name__)


@login_required
def access(request, id):
    """
    Returns json of access right for a given node
    """
    try:
        node = BaseTreeNode.objects.get(id=id)
    except BaseTreeNode.DoesNotExist:
        raise Http404("Node does not exists")

    if not request.user.has_perm(Access.PERM_READ, node):
        return HttpResponseForbidden()

    result = []
    if request.method == 'GET':
        for acc in node.access_set.all():
            item = {}
            if acc.user:
                item['name'] = acc.user.username
                item['model'] = 'user'
            if acc.group:
                item['name'] = acc.group.name
                item['model'] = 'group'

            item['access_type'] = acc.access_type
            item['access_inherited'] = acc.access_inherited
            item['permissions'] = get_access_perms_as_hash(
                node,
                item['model'],
                item['name']
            )

            result.append(item)
    if request.method == 'POST':
        if request.is_ajax():
            if not request.user.has_perm(Access.PERM_CHANGE_PERM, node):
                return HttpResponseForbidden()
            #
            # json data of following format is expected:
            #   {
            #     'add': [
            #        {
            #           'model': 'user',
            #           'name': 'margaret',
            #           'access_type': 'allow',
            #           'permissions': {
            #               'read': true, 'write': true, 'delete': false
            #           }
            #        }
            #      ],
            #    'delete': [
            #        {
            #            'model': 'user',
            #            'name': 'uploader',
            #            'access_type': 'allow',
            #            'permissions': {  // does not matter,
            #                'read': true
            #            }
            #        }
            #   ]
            #   }
            #

            access_data = json.loads(request.body)
            if 'add' in access_data.keys():
                access_diffs = set_access_perms(
                    node,
                    access_data['add']
                )
                node.propagate_changes(
                    diffs_set=access_diffs,
                    apply_to_self=False
                )
            if 'delete' in access_data.keys():
                access_diffs = delete_access_perms(
                    node,
                    access_data['delete']
                )
                node.propagate_changes(
                    diffs_set=access_diffs,
                    apply_to_self=False
                )
        else:  # POST but not ajax
            return HttpResponseBadRequest()

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


@login_required
def user_or_groups(request):
    """
    Returns list of user and groups to be displayed in
    permission editor for any document/folder
    """
    result = []
    for user in User.objects.order_by('username').all():
        item = {}
        item['model'] = 'user'
        item['name'] = user.username
        result.append(item)

    for group in Group.objects.order_by('name').all():
        item = {}
        item['model'] = 'group'
        item['name'] = group.name
        result.append(item)

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )
