from django.utils.translation import ugettext_lazy as _
from papermerge.core.views import (
    AdminListView,
    AdminChangeView
)


from papermerge.contrib.admin.models import LogEntry
from papermerge.contrib.admin.forms import LogEntryForm


class LogsListView(AdminListView):
    model_class = LogEntry
    model_label = 'admin.LogEntry'
    template_name = 'admin/log_entries.html'
    list_url = 'admin:logs'
    permissions = {
        'can_add': lambda user: user.has_perm('admin.add_logentry'),
        'can_change': lambda user: user.has_perm('admin.change_logentry'),
        'can_delete': lambda user: user.has_perm('admin.delete_logentry'),
        'can_view': lambda user: user.has_perm('admin.view_logentry'),
    }

    def get_queryset(self, request):
        if request.user.is_superuser:
            # superuser sees all logs
            return LogEntry.objects.all()

        logs = LogEntry.objects.filter(user=request.user)

        return logs


class LogChangeView(AdminChangeView):
    title = _('Log Entry')
    model_class = LogEntry
    form_class = LogEntryForm
    template_name = 'admin/log_entry.html'
    change_url = 'admin:log_change'
