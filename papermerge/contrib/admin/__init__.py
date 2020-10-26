from .registries import (
    navigation,
    user_menu_registry
)

default_app_config = 'papermerge.contrib.admin.apps.AdminConfig'

__all__ = [
    'default_app_config',
    'navigation',
    'user_menu_registry'
]
