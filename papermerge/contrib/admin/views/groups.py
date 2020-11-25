from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from papermerge.contrib.admin.forms import GroupForm
from papermerge.contrib.admin.views import mixins as mix


class GroupsView(LoginRequiredMixin):
    # only superuser can access this view
    only_superuser = True
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('admin:groups')

    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            if not self._is_allowed(request):
                raise PermissionDenied()

        ret = super().dispatch(request, *args, **kwargs)

        return ret

    def _is_allowed(self, request):
        if hasattr(self, 'only_superuser'):
            if getattr(self, 'only_superuser'):
                return request.user.is_superuser

        return True


class GroupsListView(
    GroupsView,
    mix.PaginationMixin,
    mix.DeleteEntriesMixin,
    generic.ListView
):
    title = _("Groups")

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.order_by('name')


class GroupCreateView(GroupsView, generic.CreateView):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('New')
        context['action_url'] = reverse_lazy('admin:group-add')

        return context


class GroupUpdateView(GroupsView, generic.UpdateView):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit')
        context['action_url'] = reverse_lazy(
            'admin:group-update',
            args=(self.object.pk,)
        )

        return context
