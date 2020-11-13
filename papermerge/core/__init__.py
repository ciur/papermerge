from .utils import get_version

default_app_config = 'papermerge.core.apps.CoreConfig'

FINAL = 'final'
ALPHA = 'alpha'
BETA = 'beta'
RC = 'rc'

VERSION = (2, 0, 0, ALPHA, 0)

__version__ = get_version(VERSION)

