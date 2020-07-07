import logging

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from papermerge.core.models import User
from papermerge.core.forms import UserForm

logger = logging.getLogger(__name__)


@login_required
def users_view(request):

    if request.method == 'POST':
        selected_action = request.POST.getlist('_selected_action')
        go_action = request.POST['action']

        if go_action == 'delete_selected':
            User.objects.filter(
                digest__in=selected_action
            ).delete()

    users = User.objects.all()

    return render(
        request,
        'admin/users.html',
        {
            'users': users,
        }
    )


@login_required
def user_view(request):
    """
    Used for new users
    """
    action_url = reverse('core:user')

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('core:users')

    form = UserForm()

    return render(
        request,
        'admin/user.html',
        {
            'form': form,
            'action_url': action_url,
            'title': _('New User')
        }
    )


@login_required
def user_change_view(request, id):
    """
    Used to edit existing users
    """
    user = get_object_or_404(User, id=id)
    action_url = reverse('core:user_change', args=(id,))

    form = UserForm(
        request.POST or None, instance=user
    )

    if form.is_valid():
        form.save()
        return redirect('core:users')

    return render(
        request,
        'admin/user.html',
        {
            'form': form,
            'action_url': action_url,
            'title': _('Edit User')
        }
    )
