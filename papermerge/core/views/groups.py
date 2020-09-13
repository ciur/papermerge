import logging

from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from papermerge.core.forms import GroupForm
from papermerge.core.views import (
    AdminListView,
    AdminView,
    AdminChangeView
)

logger = logging.getLogger(__name__)


class GroupListView(AdminListView):
    model_class = Group
    model_label = 'auth.Group'
    template_name = 'admin/groups.html'
    list_url = 'core:groups'

    def get_queryset(self, request):
        return self.model_class.objects.order_by('name')


class GroupView(AdminView):
    title = _('New Group')
    model_class = Group
    form_class = GroupForm
    template_name = 'admin/group.html'
    action_url = 'core:group'
    list_url = 'core:groups'


class GroupChangeView(AdminChangeView):
    title = _('Edit Group')
    model_class = Group
    form_class = GroupForm
    template_name = 'admin/group.html'
    change_url = 'core:group_change'
    list_url = 'core:groups'
