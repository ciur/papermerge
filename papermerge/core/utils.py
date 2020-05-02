import logging
import re
import subprocess
import os

from django.conf import settings
from django.apps import apps
from papermerge.core.models import User

logger = logging.getLogger(__name__)


def get_superuser():
    user = User.objects.filter(
        is_superuser=True
    ).first()

    return user


def get_sql_content(file_name):
    """
    Returns SQL statements from
    papermerge/core/pgsql/*.sql files

    Used in :
        1. data migration 0002_auto from core app.
        2. update_fts core command
    """
    core_path = apps.get_app_config('core').path
    full_sql_file_path = os.path.join(
        core_path,
        "pgsql",
        file_name
    )
    if not os.path.exists(full_sql_file_path):
        logger.debug(f"file {full_sql_file_path} not found")
        return

    sql_content = None
    with open(full_sql_file_path, 'rt') as f:
        sql_content = f.read()
        logger.debug(sql_content)
        return sql_content

    if not sql_content:
        logger.debug(f"No SQL content available. Aborting.")
        return


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
