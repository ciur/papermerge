from datetime import timedelta
import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from knox.models import AuthToken
from papermerge.core.forms import AuthTokenForm

logger = logging.getLogger(__name__)


@login_required
def tokens_view(request):

    if request.method == 'POST':
        selected_action = request.POST.getlist('_selected_action')
        go_action = request.POST['action']

        if go_action == 'delete_selected':
            AuthToken.objects.filter(
                digest__in=selected_action
            ).delete()

    tokens = AuthToken.objects.all()

    return render(
        request,
        'admin/tokens.html',
        {
            'tokens': tokens,
        }
    )


@login_required
def token_view(request):

    if request.method == 'POST':

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

    form = AuthTokenForm()

    return render(
        request,
        'admin/token.html',
        {
            'form': form,
        }
    )
