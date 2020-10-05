import functools
import os
import subprocess
import time
import logging
import re
from datetime import datetime

from django.utils.html import format_html
from django.urls import reverse


logger = logging.getLogger(__name__)


def date_2int(kv_format, str_value):
    # maps PAPERMERGE_METADATA_DATE_FORMATS to
    # https://docs.python.org/3.8/library/datetime.html#strftime-and-strptime-format-codes

    if not str_value:
        return 0

    format_map = {
        'dd.mm.yy': '%d.%m.%y',
        'dd.mm.yyyy': '%d.%m.%Y',
        'dd.M.yyyy': '%d.%B.%Y',
        'month': '%B'
    }
    try:
        _date_instance = datetime.strptime(
            str_value, format_map[kv_format]
        )
    except Exception as e:
        # this is expected because of automated
        # extraction of metadata may fail.
        logger.debug(
            f"While converting date user format {e}"
        )
        return 0

    return _date_instance.timestamp()


def money_2int(kv_format, str_value):
    return number_2int(kv_format, str_value)


def number_2int(kv_format, str_value):
    """
    kv_format for number is usually something like this:

        dddd
        d,ddd
        d.ddd

    So converting to an integer means just remove from string
    non-numeric characters and cast remaining str to integer.
    """
    if str_value:
        line = re.sub(r'[\,\.]', '', str_value)
        return line

    return 0


def node_tag(node):

    node_url = reverse("core:node", args=(node.id,))
    tag = format_html(
        "<a href='{}'>{}</a>",
        node_url,
        node.title
    )

    return tag


def document_tag(node):

    node_url = reverse("core:document", args=(node.id,))
    tag = format_html(
        "<a href='{}'>{}</a>",
        node_url,
        node.title
    )

    return tag


class Timer:
    """
    Timer class used to measure how much time
    certain code block took to complete.

    Example:

        with Timer() as t:
            main_ocr_page(...)

        logger.info(
            f"OCR took {t:.2f} seconds to complete"
        )
    """

    def __init__(self):
        self.total = None

    def __enter__(self):
        self.start = time.time()
        # important, because 'as' variable
        # is assigned only the result of __enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        self.total = self.end - self.start

    def __str__(self):
        return f"{self.total:.2f}"


def get_version(version=None):
    """Return a PEP 440-compliant version number from VERSION."""
    version = get_complete_version(version)

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|rc}N - for alpha, beta, and rc releases

    main = get_main_version(version)

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        git_changeset = get_git_changeset()
        if git_changeset:
            sub = '.dev%s' % git_changeset

    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'rc'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub


def get_main_version(version=None):
    """Return main version (X.Y[.Z]) from VERSION."""
    version = get_complete_version(version)
    parts = 2 if version[2] == 0 else 3
    return '.'.join(str(x) for x in version[:parts])


def get_complete_version(version=None):
    """
    Return a tuple of the django version. If version argument is non-empty,
    check for correctness of the tuple provided.
    """
    if version is None:
        from django import VERSION as version
    else:
        assert len(version) == 5
        assert version[3] in ('alpha', 'beta', 'rc', 'final')

    return version


@functools.lru_cache()
def get_git_changeset():
    """Return a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
    git_log = subprocess.run(
        ['git', 'log', '--pretty=format:%ct', '--quiet', '-1', 'HEAD'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=repo_dir,
    )
    timestamp = git_log.stdout
    try:
        timestamp = datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return None
    return timestamp.strftime('%Y%m%d%H%M%S')


def filter_node_id(value):
    """Invalid values of node id will be
    filtered out (return None).

    Valid values for node id will pass
    and will be returned as integers.
    """
    if not value:
        return None

    if isinstance(value, str):
        if value.isnumeric():
            return int(value)
        return None

    if isinstance(value, int):
        if value < 0:
            return None

        return value

    return None


def remove_backup_filename_id(value: str) -> str:
    """
    value is a string that looks like something__number,
    i.e. consists of two parts separated by double underscore.
    Second part (__number) is a number.
    Examples:

        blah.pdf__23
        boo__1
        asdlaksd__100

    This function returns first part of the string:

    value: blah.pdf__23 => result: blah.pdf
           boo__1  => boo

    Other examples:

        boox_1       => boox
        boox         => boox
        boox_____100 => boox
        None         => None
    """
    # works only with string input
    if not value:
        return None

    if not isinstance(value, str):
        return value

    result = value.split('_')

    if len(result) <= 2:
        return result[0]

    return "_".join(result[0:-2])
