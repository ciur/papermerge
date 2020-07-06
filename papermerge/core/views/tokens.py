import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from knox.models import AuthToken

logger = logging.getLogger(__name__)


@login_required
def tokens_view(request):

    tokens = AuthToken.objects.all()

    return render(
        request,
        'admin/tokens.html',
        {
            'tokens': tokens,
        }
    )
