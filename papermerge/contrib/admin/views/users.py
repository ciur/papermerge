from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from papermerge.core.models import User
from papermerge.contrib.admin.forms import UserFormWithPassword
from papermerge.core.views import (
    PaginationMixin,
    DeleteEntriesMixin
)


class UsersView(LoginRequiredMixin):
    # only superuser can access this view
    only_superuser = True
    model = User
    form_class = UserFormWithPassword
    success_url = reverse_lazy('admin:users')

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


class UsersListView(
    UsersView,
    PaginationMixin,
    DeleteEntriesMixin,
    ListView
):
    title = _("Users")

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.order_by('username')


class UserCreateView(UsersView, CreateView):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('New')
        context['action_url'] = reverse_lazy('admin:user-add')

        return context


class UserUpdateView(UsersView, UpdateView):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit')
        context['action_url'] = reverse_lazy(
            'admin:user-update',
            args=(self.object.pk,)
        )

        return context
