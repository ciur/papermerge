from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from papermerge.core.models import Role
from papermerge.contrib.admin.forms import RoleForm
from papermerge.contrib.admin.views import mixins as mix


class RolesView(
    LoginRequiredMixin,
    mix.RequiredPermissionMixin
):
    # only superuser can access this view
    only_superuser = True
    model = Role
    form_class = RoleForm
    success_url = reverse_lazy('admin:roles')

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


class RolesListView(
    RolesView,
    mix.PaginationMixin,
    mix.DeleteEntriesMixin,
    generic.ListView
):
    title = _("Roles")
    required_permission = 'core.view_role'

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.order_by('name')


class RoleCreateView(RolesView, generic.CreateView):

    required_permission = 'core.add_role'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('New')
        context['action_url'] = reverse_lazy('admin:role-add')

        return context


class RoleUpdateView(RolesView, generic.UpdateView):

    required_permission = 'core.change_role'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit')
        context['action_url'] = reverse_lazy(
            'admin:role-update',
            args=(self.object.pk,)
        )

        return context
