from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from papermerge.contrib.admin.forms import GroupForm
from papermerge.core.views import (
    AdminListView,
    AdminView,
    AdminChangeView
)


class GroupsListView(AdminListView):
    # only superuser can list groups
    only_superuser = True
    model_class = Group
    model_label = 'auth.Group'
    template_name = 'admin/groups.html'
    list_url = 'admin:groups'
    permissions = {
        'can_add': lambda user: user.has_perm('admin.add_group'),
        'can_change': lambda user: user.has_perm('admin.change_group'),
        'can_delete': lambda user: user.has_perm('admin.delete_group'),
        'can_view': lambda user: user.has_perm('admin.view_group'),
    }

    def get_queryset(self, request):
        return self.model_class.objects.order_by('name')


class GroupView(AdminView):
    # only superuser can view group(s)
    only_superuser = True
    title = _('New Group')
    model_class = Group
    form_class = GroupForm
    template_name = 'admin/group.html'
    action_url = 'admin:group'
    list_url = 'admin:groups'


class GroupChangeView(AdminChangeView):
    # only superuser can edit group(s)
    only_superuser = True
    title = _('Edit Group')
    model_class = Group
    form_class = GroupForm
    template_name = 'admin/group.html'
    change_url = 'admin:group_change'
    list_url = 'admin:groups'
