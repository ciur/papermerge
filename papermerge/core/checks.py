import os
import shutil

from django.conf import settings
from django.core.checks import Error, Warning, register


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
