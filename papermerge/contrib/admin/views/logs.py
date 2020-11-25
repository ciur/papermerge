from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy


from papermerge.contrib.admin.models import LogEntry
from papermerge.contrib.admin.forms import LogEntryForm
from papermerge.contrib.admin.views import mixins as mix


class LogsView(LoginRequiredMixin):
    model = LogEntry
    form_class = LogEntryForm
    success_url = reverse_lazy('admin:logs')


class LogsListView(
    LogsView,
    mix.PaginationMixin,
    mix.DeleteEntriesMixin,
    generic.ListView
):

    title = _("Logs")

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_superuser:
            # superuser sees all logs
            return qs.all()

        logs = qs.filter(user=self.request.user)

        return logs


class LogUpdateView(LogsView, generic.UpdateView):

    title = _("Log Entry")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = self.title

        return context

