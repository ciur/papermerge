from .registries import (
    navigation,
    user_menu_registry,
    sidebar
)

default_app_config = 'papermerge.contrib.admin.apps.AdminConfig'

__all__ = [
    'default_app_config',
    'navigation',
    'sidebar',
    'user_menu_registry',
    'SidebarPart',
]

class SidebarPart:

    """
    Wrapper class for managing/rendering document parts
    on sidebar.
    """

    def __init__(self, document):
        # papermerge.core.models.document instance
        self.document = document

    def to_json(self):
        pass
