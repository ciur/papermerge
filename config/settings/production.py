from .base import *  # noqa

# Achtung!
DEBUG = False

# include additional apps used in production
# only
INSTALLED_APPS.extend(
    ['mod_wsgi.server', ]
)
