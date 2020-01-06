from django.core.management.base import BaseCommand
from django.core.management import (
    call_command,
)
from django_tenants.utils import get_tenant_model


class Command(BaseCommand):
    help = "Runs given django command on each tenant in the system."

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

        #parser.add_argument(
        #    'command_name',
        #    help='The command name you want to run'
        #)

    def handle(self, *args, **options):
        #command_name = options.get('command_name')
        TenantModel = get_tenant_model()
        for tenant in TenantModel.objects.all():
            call_command(
                'tenant_command',
                'indexupdate',
                schema=tenant.name
            )
