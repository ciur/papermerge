import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from papermerge.core.models import BaseTreeNode

logger = logging.getLogger(__name__)


@login_required
def metadata(request, id):
    try:
        node = BaseTreeNode.objects.get(id=id)
    except BaseTreeNode.DoesNotExist:
        raise Http404("Node does not exists")

    kvstore = []
    kvstore_comp = []

    if request.method == 'GET':
        for kv in node.kv.all():
            item = {}
            item['id'] = kv.id
            item['key'] = kv.key
            item['inherited'] = kv.kv_inherited
            kvstore.append(item)
        for kv in node.kvcomp.all():
            item = {}
            item['id'] = kv.id
            item['key'] = kv.key
            item['inherited'] = kv.kv_inherited
            kvstore_comp.append(item)
    else:
        kv_data = json.loads(request.body)
        if 'kvstore' in kv_data:
            if isinstance(kv_data['kvstore'], list):
                node.kv.update(kv_data['kvstore'])
        if 'kvstore_comp' in kv_data:
            if isinstance(kv_data['kvstore_comp'], list):
                node.kvcomp.update(kv_data['kvstore_comp'])

    return HttpResponse(
        json.dumps(
            {
                'kvstore': kvstore,
                'kvstore_comp': kvstore_comp
            }
        ),
        content_type="application/json"
    )
