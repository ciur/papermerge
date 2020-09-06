from django.apps import AppConfig


class AdminConfig(AppConfig):
    name = 'papermerge.contrib.admin'

    def ready(self):
        from papermerge.contrib.admin import signals  # noqa
