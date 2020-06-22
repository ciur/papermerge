import shutil

from django.conf import settings
from django.core.checks import Warning, register


@register()
def papermerge_configuration_file(app_configs, **kwargs):

    check_messages = []
    places = ''

    if settings.DEFAULT_CONFIG_PLACES:
        places = ', '.join(settings.DEFAULT_CONFIG_PLACES)

    warn_message = "papermerge.conf.py file was found." +\
        f" Following locations attempted {places}"

    hint_msg = "Create one of those files or point" +\
        f" {settings.DEFAULT_PAPERMERGE_CONFIG_ENV_NAME}" +\
        " environment name to it."

    if not settings.CFG_PAPERMERGE:
        check_messages.append(
            Warning(warn_message, hint_msg)
        )

    return check_messages


@register()
def binaries_check(app_configs, **kwargs):
    """
    Papermerge requires the existence of a few binaries, so we do some checks
    for those here.
    """

    error = "Papermerge can't find {}. Without it, OCR of the documents is impossible."
    hint = "Either it's not in your ${PATH} or it's not installed."

    binaries = (
        "tesseract",
    )

    check_messages = []
    for binary in binaries:
        if shutil.which(binary) is None:
            check_messages.append(Warning(error.format(binary), hint))

    return check_messages
