from django.utils.module_loading import import_string

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


def get_search_backend(import_path=None):
    backend = import_path or settings.PAPERMERGE_SEARCH_BACKEND
    try:
        backend_cls = import_string(backend)
    except ImportError as e:
        raise ImproperlyConfigured("Could not find backend '%s': %s" % (
            backend, e))

    # Create backend
    return backend_cls()
