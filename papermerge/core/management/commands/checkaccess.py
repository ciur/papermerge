import logging
from django.core.management.base import BaseCommand

from papermerge.core.models import (
    BaseTreeNode,
    Access
)
from papermerge.core.auth import (
    create_access_perms
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Lists/Updates Access Models associated with nodes.
"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            '-c',
            action="store_true",
            help="Count nodes with/without associated access model."
        )
        parser.add_argument(
            '--update',
            '-u',
            action="store_true",
            help="Updated nodes without associated access model."
        )

    def run_count(
        self,
    ):
        total_count = BaseTreeNode.objects.count()
        without_access_count = BaseTreeNode.objects.filter(
            access__isnull=True
        ).count()

        print(
            f"total={total_count}, without_access={without_access_count}"
        )

    def run_update(
        self
    ):
        perms = create_access_perms()

        for node in BaseTreeNode.objects.all():
            if node.access_set.count() == 0:
                access = Access.objects.create(
                    user=node.user,
                    access_type='allow',
                    node=node
                )
                access.permissions.add(*perms)

    def handle(self, *args, **options):
        count = options.get(
            'count',
            False
        )
        update = options.get(
            'update',
            False
        )
        if count:
            self.run_count()
        elif update:
            self.run_update()
