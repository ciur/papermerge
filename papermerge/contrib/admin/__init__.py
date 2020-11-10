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
    'user_menu_registry'
]
