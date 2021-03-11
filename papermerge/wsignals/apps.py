from django.apps import AppConfig


class WsignalsConfig(AppConfig):
    # Worker signals app
    name = 'papermerge.wsignals'
    label = 'wsignals'

    def ready(self):
        from papermerge.wsignals import signals  # noqa
