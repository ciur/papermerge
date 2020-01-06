import os
import logging
from django.core.management.base import BaseCommand
from django.apps import apps

try:
    from django_tenants.utils import get_tenant_model
except:
    get_tenant_model = None

from django.db import connection

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Run specified SQL file in all schemas.
"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--file-name',
            '-f',
            help="SQL file name"
        )
        parser.add_argument(
            '--schema-name',
            '-s',
            help="Run sql command only on this schema"
        )

    def run_sql(
        self,
        tenant_name=None,
        sql_content=None
    ):
        logger.debug(f"Executing for tenant {tenant_name}")
        with connection.cursor() as c:
            c.execute(sql_content)

    def handle(self, *args, **options):
        file_name = options.get(
            'file_name',
            False
        )
        schema_name = options.get('schema_name', False)
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

        if not sql_content:
            logger.debug(f"No SQL content available. Aborting.")
            return

        TenantModel = get_tenant_model()

        if schema_name:
            tenant_list = TenantModel.objects.filter(name=schema_name)
        else:
            tenant_list = TenantModel.objects.exclude(name="public")

        for tenant in tenant_list:
            connection.set_tenant(tenant)
            self.run_sql(
                tenant_name=tenant.name,
                sql_content=sql_content
            )
