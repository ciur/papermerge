from datetime import timedelta
import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from knox.models import AuthToken
from papermerge.contrib.admin.forms import AuthTokenForm

logger = logging.getLogger(__name__)


@login_required
def tokens_view(request):

    if request.method == 'POST':
        selected_action = request.POST.getlist('_selected_action')
        go_action = request.POST['action']

        if go_action == 'delete_selected':
            if request.user.has_perm('knox.delete_authtoken'):
                AuthToken.objects.filter(
                    digest__in=selected_action
                ).delete()
            else:
                messages.info(
                    request,
                    _("You don't have %(model)s %(delete)s permissions") % {
                        'delete': _('delete'),
                        'model': _('token')
                    }
                )

    tokens = AuthToken.objects.filter(user=request.user)

    return render(
        request,
        'admin/tokens.html',
        {
            'tokens': tokens,
            'has_perm_add_authtoken': request.user.has_perm(
                'knox.add_authtoken'
            )
        }
    )


@login_required
def token_view(request):

    if request.method == 'POST':
        if request.user.has_perm('knox.add_authtoken'):
            form = AuthTokenForm(request.POST)

            if form.is_valid():
                instance, token = AuthToken.objects.create(
                    user=request.user,
                    expiry=timedelta(hours=form.cleaned_data['hours'])
                )
                html_message = "Please remember the token: "
                html_message += f" <span class='text-success'>{token}</span>"
                html_message += " It won't be displayed again."
                messages.success(
                    request, html_message
                )

                return redirect('core:tokens')
        else:
            messages.info(
                request,
                _("You don't have %(model)s %(add)s permissions") % {
                    'add': _('add'),
                    'model': _('token')
                }
            )

    form = AuthTokenForm()

    return render(
        request,
        'admin/token.html',
        {
            'form': form,
            'has_perm_add_authtoken': request.user.has_perm(
                'knox.add_authtoken'
            )
        }
    )
