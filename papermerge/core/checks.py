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

    msg = {
        "file": "Without it, Papermerge won't be able to learn file mime type",
        "convert": "Without it, image resizing is not possible",
        "pdftoppm": "Without it, it not possible to extract images from PDF",
        "tesseract": "Without it, OCR of the documents is impossible",
        "identify": "Without it, it is not possible to count pages in TIFF",
        "pdfinfo": "Without it, Papermerge won't function properly",
        "pdftk": "Without it, Papermerge won't be able to cut/paste PDF pages"
    }
    error = "Papermerge can't find {}. {}."
    hint = "Either it's not in your PATH or it's not installed."

    check_messages = []
    for binary in msg.keys():
        if shutil.which(binary) is None:
            check_messages.append(
                Warning(
                    error.format(binary, msg[binary]),
                    hint
                )
            )

    return check_messages
