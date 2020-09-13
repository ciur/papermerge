import logging

from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from papermerge.core.forms import GroupForm
from papermerge.core.views import AdminListView

logger = logging.getLogger(__name__)


class GroupListView(AdminListView):
    model_class = Group
    model_label = 'auth.Group'
    template_name = 'admin/groups.html'

    def get_queryset(self, request):
        return self.model_class.objects.order_by('name')


@login_required
def group_view(request):
    """
    Used for new groups
    """
    action_url = reverse('core:group')

    if request.method == 'POST':

        form = GroupForm(request.POST)
        if form.is_valid():

            group = Group.objects.create(
                name=form.cleaned_data['name']
            )
            if group:
                msg = "Group %(name)s was successfully created."
                messages.info(
                    request,
                    _(msg) % {'name': group.name}
                )
            return redirect('core:groups')

    form = GroupForm()

    return render(
        request,
        'admin/group.html',
        {
            'form': form,
            'action_url': action_url,
            'title': _('New Group')
        }
    )


@login_required
def group_change_view(request, id):
    """
    Used to edit existing groups
    """
    group = get_object_or_404(Group, id=id)
    action_url = reverse('core:group_change', args=(id,))

    form = GroupForm(
        request.POST or None, instance=group
    )

    if form.is_valid():
        form.save()
        return redirect('core:groups')

    return render(
        request,
        'admin/group.html',
        {
            'form': form,
            'action_url': action_url,
            'title': _('Edit Group')
        }
    )
