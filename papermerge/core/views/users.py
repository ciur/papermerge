import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            instance, user = User.objects.create(
                form.cleaned_data
            )
            return redirect('core:users')

    form = UserForm()

    return render(
        request,
        'admin/user.html',
        {
            'form': form,
        }
    )
