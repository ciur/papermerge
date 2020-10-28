from .utils import get_version

default_app_config = 'papermerge.core.apps.CoreConfig'

FINAL = 'final'
ALPHA = 'alpha'
BETA = 'beta'
RC = 'rc'

VERSION = (1, 5, 1, ALPHA, 0)

__version__ = get_version(VERSION)

