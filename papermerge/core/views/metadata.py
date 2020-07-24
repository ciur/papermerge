import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from papermerge.core.models import BaseTreeNode, Page
from papermerge.core.models.kvstore import (get_currency_formats,
                                            get_date_formats, get_kv_types,
                                            get_numeric_formats)

logger = logging.getLogger(__name__)


@login_required
def metadata(request, model, id):
    """
    model can be either node or page. Respectively
    id will be the 'id' of either node or page.
    """
    if model == 'node':
        _Klass = BaseTreeNode
    else:
        _Klass = Page
    try:
        item = _Klass.objects.get(id=id)
    except _Klass.DoesNotExist:
        raise Http404("Node does not exists")

    kvstore = []

    if request.method == 'GET':
        for kv in item.kv.all():
            kvstore.append(kv.to_dict())
    else:
        kv_data = json.loads(request.body)
        if 'kvstore' in kv_data:
            if isinstance(kv_data['kvstore'], list):
                item.kv.update(
                    _sanitize_kvstore_list(kv_data['kvstore'])
                )

    return HttpResponse(
        json.dumps(
            {
                'kvstore': kvstore,
                'currency_formats': get_currency_formats(),
                'date_formats': get_date_formats(),
                'numeric_formats': get_numeric_formats(),
                'kv_types': get_kv_types()

            }
        ),
        content_type="application/json"
    )


def _sanitize_kvstore_list(kvstore_list):
    """
    Creates a new dictionay only with allowed keys.
    """
    new_kvstore_list = []
    allowed_keys = ['key', 'kv_inherited', 'value', 'kv_type']

    for item in kvstore_list:
        sanitized_kvstore_item = {
            allowed_key: item[allowed_key] for allowed_key in allowed_keys
        }
        new_kvstore_list.append(sanitized_kvstore_item)

    return new_kvstore_list
