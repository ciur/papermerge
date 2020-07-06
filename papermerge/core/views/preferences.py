import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from dynamic_preferences.users.forms import user_preference_form_builder


logger = logging.getLogger(__name__)


@login_required
def preferences_view(request):

    Form = user_preference_form_builder(instance=request.user)

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            form.update_preferences()
            return redirect('index')

    return render(
        request,
        'admin/preferences.html',
        {
            'form': Form,
        }
    )
