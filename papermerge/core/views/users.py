import logging

from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseForbidden

from papermerge.core.models import User, AuthenticationSource
from papermerge.contrib.admin.forms import (
    UserFormWithoutPassword,
    UserFormWithPassword
)

logger = logging.getLogger(__name__)


@login_required
def users_view(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    can_add_users = AuthenticationSource.can_change_data(request.user.authentication_source) and request.user.has_perm('core.add_user')
    can_delete_users = request.user.has_perm('core.delete_user')

    if request.method == 'POST':
        selected_action = request.POST.getlist('_selected_action')
        go_action = request.POST['action']

        if go_action == 'delete_selected' and can_delete_users:
            User.objects.filter(
                id__in=selected_action
            ).delete()

    users = User.objects.all()

    return render(
        request,
        'admin/users.html',
        {
            'users': users,
            'can_add_users': can_add_users,
            'can_delete_users': can_delete_users,
        }
    )


@login_required
def user_view(request):
    """
    When adding a new user, administrator will need to add
    username + password and then he/she will be able to edit further
    details.
    """

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    form = UserFormWithPassword()

    if request.method == 'POST':
        form = UserFormWithPassword(request.POST)
        if form.is_valid():

            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 == password2:

                user = form.save()
                user.set_password(password1)
                user.save()

                return redirect(
                    reverse('core:user_change', args=(user.id, ))
                )
            else:
                form.add_error(
                    'password1',
                    _('Password and Password confirmation does not match')
                )

    return render(
        request,
        'admin/add_user.html',
        {
            'form': form,
        }
    )


@login_required
def user_change_view(request, id):
    """
    Used to edit existing users
    """

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    user = get_object_or_404(User, id=id)
    action_url = reverse('core:user_change', args=(id,))
    user.can_change_data = AuthenticationSource.can_change_data(user.authentication_source) and request.user.has_perm('core.change_user')

    form = UserFormWithoutPassword(
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
            'title': _('Edit User'),
            'user_id': id,
            'can_change_user_data': user.can_change_data,
            'user_authentication_source': user.authentication_source,
        }
    )


@login_required
def user_change_password_view(request, id):
    """
    This view is used by administrator to change password of ANY user in the
    system. As result, 'current password' won't be asked.
    """

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    user = get_object_or_404(User, id=id)
    user.can_change_data = AuthenticationSource.can_change_data(user.authentication_source) and request.user.has_perm('core:change_user')
    action_url = reverse('core:user_change_password', args=(id,))

    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not user.can_change_data:
            messages.error(
                request,
                _("Password of user cannot be changed, because it was imported from %s." % user.authentication_source)
            )
            return redirect(
                reverse('core:user_change', args=(id,))
            )
        elif password1 == password2:
            user.set_password(password1)
            user.save()
            messages.success(
                request,
                _("Password was successfully changed.")
            )
            return redirect(
                reverse('core:user_change', args=(id,))
            )

    return render(
        request,
        'admin/user_change_password.html',
        {
            'user': user,
            'action_url': action_url
        }
    )
