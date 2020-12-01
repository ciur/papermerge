import os
import subprocess

from django.conf import settings
from django.core.checks import Warning, register

from papermerge.core.importers.imap import login as imap_login


USED_BINARIES = {
    settings.BINARY_FILE: {
        "msg": (
            "Without it, Papermerge won't be"
            " "
            "able to learn file mime type"),
        "option": "-v"
    },
    settings.BINARY_CONVERT: {
        "msg": (
            "Without it, image resizing is not possible"
        ),
        "option": "-v"
    },
    settings.BINARY_PDFTOPPM: {
        "msg": (
            "Without it, it not possible to extract images from PDF"
        ),
        "option": "-v"
    },
    settings.BINARY_OCR: {
        "msg": (
            "Without it, OCR of the documents is impossible"
        ),
        "option": "-v"
    },
    settings.BINARY_IDENTIFY: {
        "msg": (
            "Without it, it is not possible to count pages in TIFF"
        ),
        "option": "-v"
    },
    settings.BINARY_PDFINFO: {
        "msg": (
            "Without it, Papermerge won't function properly."
            " "
            "It won't be able to find out PDF files page count"
        ),
        "option": "-v"
    },
    settings.BINARY_STAPLER: {
        "msg": (
            "Without it, Papermerge won't be able to cut/paste PDF pages"
        ),
        "option": "-version"
    }
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

    warn_message = "papermerge.conf.py file was not found." +\
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
    if required binaries are available.

    See settings prefixed with BINARY_ defined in mglib.conf.default_settings
    for full list of dependencies.
    """
    error = "Papermerge can't find {}. {}."
    hint = "Either it's not in your PATH or it's not installed."

    check_messages = []
    for binary_path in USED_BINARIES.keys():

        binary = os.path.basename(binary_path)
        option = USED_BINARIES[binary_path]["option"]
        try:
            subprocess.run(
                [binary_path, option],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            check_messages.append(
                Warning(
                    error.format(binary, USED_BINARIES[binary_path]["msg"]),
                    hint
                )
            )

    return check_messages


@register()
def imap_login_check(app_configs, **kwargs):

    host = settings.PAPERMERGE_IMPORT_MAIL_HOST
    user = settings.PAPERMERGE_IMPORT_MAIL_USER
    password = settings.PAPERMERGE_IMPORT_MAIL_PASS

    check_messages = []
    msg = f"Failed to login to IMAP server '{host}'"
    hint = """
        Please double check that IMPORT_MAIL_HOST,
        IMPORT_MAIL_USER, IMPORT_MAIL_PASS settings
        are correct.
    """

    if all([host, user, password]):
        try:
            server = imap_login(
                imap_server=host,
                username=user,
                password=password
            )
        except Exception:
            server = None

        if not server:
            check_messages.append(
                Warning(
                    msg,
                    hint
                )
            )

    return check_messages
