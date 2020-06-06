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

    result = []

    if request.method == 'GET':
        for kv in node.kv.all():
            item = {}
            item['id'] = kv.id
            item['key'] = kv.key
            item['inherited'] = kv.inherited
            result.append(item)
    else:
        # POST here
        pass

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )
