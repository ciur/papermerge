from django.core.management.base import (
    BaseCommand,
    CommandError
)
from django.contrib.auth.models import User
from django.db import connection

from papermerge.boss.users import create_boss_perms

try:
    from django_tenants.utils import (
        get_tenant_model,
    )
except ModuleNotFoundError as e:
    # means, we deal with onprem version
    TenantModel = None
else:
    TenantModel = get_tenant_model()


class Command(BaseCommand):

    help = """
    Create boss group (name defined by settings.VML_BOSS_USER_GROUP).
    If an existing user is passed as arguments it will add that user to the
    group.
"""

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--schemaname',
            help='Name of the company where to create root user',
            nargs='?',
            default='public'
        )
        parser.add_argument(
            'username',
            help='Username of root user to create'
        )
        parser.add_argument(
            "email",
            help="Email for administrative user",
        )
        parser.add_argument(
            "password",
            help="Password for administrative user",
        )

    def handle(self, *args, **options):
        schemaname = options['schemaname']

        if schemaname != 'public' and TenantModel:
            tenant = None
            try:
                tenant = TenantModel.objects.get(schema_name=schemaname)
            except TenantModel.DoesNotExist:
                raise CommandError(
                    "There are no tenants with name %s" % schemaname
                )
            connection.set_tenant(tenant)

        username = options['username']
        email = options['email']
        password = options['password']

        boss_access, boss_root = create_boss_perms()

        user, _ = User.objects.get_or_create(
            username=username,
            email=email
        )

        user.set_password(password)
        user.save()

        if user:
            user.user_permissions.add(boss_access)
            user.user_permissions.add(boss_root)
