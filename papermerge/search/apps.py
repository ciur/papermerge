from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PapermergeSearchConfig(AppConfig):
    name = 'papermerge.search'
    label = 'papermergesearch'
    verbose_name = _("Papermerge search")
