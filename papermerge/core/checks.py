import os
import shutil

from django.conf import settings
from django.core.checks import Warning, register

from mglib.conf import default_settings

USED_BINARIES = {
    default_settings.BINARY_FILE: (
        "Without it, Papermerge won't be"
        " "
        "able to learn file mime type"
    ),
    default_settings.BINARY_CONVERT: (
        "Without it, image resizing is not possible"
    ),
    default_settings.BINARY_PDFTOPPM: (
        "Without it, it not possible to extract images from PDF"
    ),
    default_settings.BINARY_OCR: (
        "Without it, OCR of the documents is impossible"
    ),
    default_settings.BINARY_IDENTIFY: (
        "Without it, it is not possible to count pages in TIFF"
    ),
    default_settings.BINARY_PDFINFO: (
        "Without it, Papermerge won't function properly."
        " "
        "It won't be able to find out PDF files page count"
    ),
    default_settings.BINARY_PDFTK: (
        "Without it, Papermerge won't be able to cut/paste PDF pages"
    )
}


@register()
def papermerge_configuration_file(app_configs, **kwargs):
    """
    Papermerge does not necessary require papermerge.conf.py file.
    However, it is a good practice to have one available - even empty!

    User/Admin defines an empty papermerge.conf.py file it means first of all
    that user/admin is aware of .conf.py file existence.

    Configuration file should be placed in projects directory, in
    /etc/papermerge.conf.py or it is file pointed by environment variable
    named PAPERMERGE_CONFIG.

    If configuration file was not found - issue a warning.
    """
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
    Papermerge requires the existence of a few binaries, so it checks
    if required binaries available.

    See settings prefixed with BINARY_ defined in mglib.conf.default_settings
    for full list of dependencies.
    """
    error = "Papermerge can't find {}. {}."
    hint = "Either it's not in your PATH or it's not installed."

    check_messages = []
    for binary_path in USED_BINARIES.keys():
        binary = os.path.basename(binary_path)
        if shutil.which(binary) is None:
            check_messages.append(
                Warning(
                    error.format(binary, USED_BINARIES[binary_path]),
                    hint
                )
            )

    return check_messages
