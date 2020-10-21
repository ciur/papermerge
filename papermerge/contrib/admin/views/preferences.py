import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from dynamic_preferences.users.forms import user_preference_form_builder
from dynamic_preferences.settings import preferences_settings


logger = logging.getLogger(__name__)


@login_required
def preferences_section_view(request, section):

    Form = user_preference_form_builder(
        instance=request.user,
        section=section
    )

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            form.update_preferences()
            return redirect('admin:preferences')

    return render(
        request,
        'admin/preferences_section.html',
        {
            'form': Form,
            'section': section
        }
    )


@login_required
def preferences_view(request):

    sections = [
        val.split(preferences_settings.SECTION_KEY_SEPARATOR)[0]
        for val in request.user.preferences.all()
    ]
    return render(
        request,
        'admin/preferences.html',
        {
            'sections': sections,
        }
    )
