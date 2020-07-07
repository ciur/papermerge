import logging

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from papermerge.core.forms import GroupForm

logger = logging.getLogger(__name__)


@login_required
def groups_view(request):

    if request.method == 'POST':
        selected_action = request.POST.getlist('_selected_action')
        go_action = request.POST['action']

        if go_action == 'delete_selected':
            Group.objects.filter(
                id__in=selected_action
            ).delete()

    groups = Group.objects.all()

    return render(
        request,
        'admin/groups.html',
        {
            'groups': groups,
        }
    )


@login_required
def group_view(request):
    """
    Used for new groups
    """
    action_url = reverse('core:group')

    if request.method == 'POST':

        form = GroupForm(request.POST)
        if form.is_valid():

            Group.objects.create(
                name=form.cleaned_data['name']
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
