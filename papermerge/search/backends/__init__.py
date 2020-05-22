from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


def import_backend(dotted_path):
    backend_module = import_module(dotted_path)
    return backend_module.SearchBackend


def get_search_backend():
    backend = getattr(settings, 'PAPERMERGE_SEARCH_BACKEND')
    # Try to import the backend
    try:
        backend_cls = import_backend(backend)
    except ImportError as e:
        raise ImproperlyConfigured("Could not find backend '%s': %s" % (
            backend, e))

    # Create backend
    return backend_cls()
