from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from papermerge.contrib.admin.views import mixins as mix
from papermerge.contrib.admin.forms import AutomateForm
from papermerge.core.models import Automate


class AutomatesView(LoginRequiredMixin):
    model = Automate
    form_class = AutomateForm
    success_url = reverse_lazy('admin:automates')


class AutomatesListView(
    AutomatesView,
    mix.PaginationMixin,
    mix.DeleteEntriesMixin,
    generic.ListView
):

    title = _("Automates")

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(
            user=self.request.user
        ).order_by('name')


class AutomateCreateView(AutomatesView, generic.CreateView):

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('New')
        context['action_url'] = reverse_lazy('admin:automate-add')

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class AutomateUpdateView(AutomatesView, generic.UpdateView):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit')
        context['action_url'] = reverse_lazy(
            'admin:automate-update',
            args=(self.object.pk,)
        )

        return context
