from datetime import timedelta

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from knox.models import AuthToken

from papermerge.contrib.admin.forms import AuthTokenForm
from papermerge.contrib.admin.views import mixins as mix


class TokensView(
    LoginRequiredMixin,
    mix.CommonListMixin
):
    model = AuthToken
    form_class = AuthTokenForm
    success_url = action_url = reverse_lazy('admin:tokens')
    new_object_url = reverse_lazy('admin:token-add')


class TokensListView(
    TokensView,
    mix.PaginationMixin,
    mix.DeleteEntriesMixin,
    generic.ListView
):
    title = _("Tokens")
    action_url = reverse_lazy('admin:tokens')

    table_header_row = [
        _('Digest'),
        _('Created At'),
        _('Expires At'),
    ]

    def get_delete_entries(self, selection):
        return self.get_queryset().filter(
            digest__in=selection
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_header_row'] = self.table_header_row
        return context


class TokenCreateView(TokensView, generic.CreateView):

    title = _("New")
    action_url = reverse_lazy('admin:token-add')
    template_name = "admin/object_form.html"

    def form_valid(self, form):

        instance, token = AuthToken.objects.create(
            user=self.request.user,
            expiry=timedelta(hours=form.cleaned_data['hours'])
        )
        html_message = f"Please remember the token: {token}"
        html_message += " It won't be displayed again."

        messages.success(
            self.request, html_message
        )
        return HttpResponseRedirect(self.success_url)

class TokenUpdateView(TokensView, generic.UpdateView):

    template_name = "admin/object_form.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit')
        context['action_url'] = reverse_lazy(
            'admin:token-update',
            args=(self.object.pk,)
        )

        return context
