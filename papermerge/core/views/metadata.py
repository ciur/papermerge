import json
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils.translation import gettext as _
from papermerge.core.models import BaseTreeNode
from papermerge.core.models.kvstore import METADATA_TYPES

logger = logging.getLogger(__name__)


def get_kv_types():
    return [
        (kv_type, _(kv_type)) for kv_type in METADATA_TYPES
    ]


def get_currency_formats():
    return [
        (currency, _(currency))
        for currency in settings.PAPERMERGE_METADATA_CURRENCY_FORMATS
    ]


def get_numeric_formats():
    return [
        (numeric, _(numeric))
        for numeric in settings.PAPERMERGE_METADATA_NUMERIC_FORMATS
    ]


def get_date_formats():
    return [
        (_date, _(_date))
        for _date in settings.PAPERMERGE_METADATA_DATE_FORMATS
    ]


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
            item['kv_inherited'] = kv.kv_inherited
            kvstore.append(item)
        for kv in node.kvcomp.all():
            item = {}
            item['id'] = kv.id
            item['key'] = kv.key
            item['kv_inherited'] = kv.kv_inherited
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
                'kvstore_comp': kvstore_comp,
                'kv_types': get_kv_types(),
                'currency_formats': get_currency_formats(),
                'numeric_formats': get_numeric_formats(),
                'date_formats': get_date_formats()
            }
        ),
        content_type="application/json"
    )
