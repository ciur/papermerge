import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from dynamic_preferences.users.forms import user_preference_form_builder

logger = logging.getLogger(__name__)


def uniq_sections(user):
    """
    Returns number of unique instances of Sections.

    I.e. returns unique instances of
        papermerge.core.preferences.Section
    """
    preferences = user.preferences
    sections = []

    # user preferences
    for key in preferences:
        section, name = preferences.parse_lookup(key)
        pref = preferences.registry.get(section=section, name=name)
        sections.append(pref.section)

    return set(sections)


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

    return render(
        request,
        'admin/preferences.html',
        {
            'sections': uniq_sections(request.user),
        }
    )
