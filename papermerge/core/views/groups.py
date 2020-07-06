import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

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
        }
    )
