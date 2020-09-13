from django.utils.translation import ugettext_lazy as _

from papermerge.core.forms import AutomateForm
from papermerge.core.models import Automate
from papermerge.core.views import (
    AdminListView,
    AdminView,
    AdminChangeView
)


class AutomatesListView(AdminListView):
    model_class = Automate
    model_label = 'core.Automate'
    template_name = 'admin/automates.html'
    list_url = 'admin:automates'

    def get_queryset(self, request):
        return self.model_class.objects.order_by('name')


class AutomateView(AdminView):
    title = _('New Automate')
    model_class = Automate
    form_class = AutomateForm
    template_name = 'admin/automate.html'
    action_url = 'admin:automate'
    list_url = 'admin:automates'


class AutomateChangeView(AdminChangeView):
    title = _('Edit Automate')
    model_class = Automate
    form_class = AutomateForm
    template_name = 'admin/automate.html'
    change_url = 'admin:automate_change'
    list_url = 'admin:automate'
