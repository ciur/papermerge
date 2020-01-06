import re
import subprocess
import os
from django.conf import settings


def escape(text, replace_with=' '):
    """
    Used when passing arbitrary text to logger
    (which passes it to pgsql).
    It leaves string with only characters which are not
    special in postgres:

    https://www.postgresql.org/docs/current/sql-syntax-lexical.html
    """
    escaped_text = re.sub(
        '[^a-zA-Z0-9 \n\.\/\_]',
        replace_with,
        text
    )
    return escaped_text


def get_media_root():
    tenant_name = get_tenant_name()
    if tenant_name:
        media_root = os.path.join(settings.MEDIA_ROOT, tenant_name)
    else:
        media_root = settings.MEDIA_ROOT

    return media_root


def get_tenant_name():
    from django.db import connection

    try:
        tenant_name = connection.get_tenant().name
    except AttributeError:
        tenant_name = None

    return tenant_name


def calc_digest(filepath):
    out = subprocess.check_output(
        ['openssl', 'sha', '-sha1', '-r', filepath]
    )
    output = out.decode("utf-8", "strict")
    sha, _ = output.split('*')

    return sha.strip()
