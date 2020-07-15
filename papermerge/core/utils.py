import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)



#def get_superuser():
#    user = User.objects.filter(
#        is_superuser=True
#    ).first()
#
#    return user

def date_2int(kv_format, str_value):
    # maps PAPERMERGE_METADATA_DATE_FORMATS to
    # https://docs.python.org/3.8/library/datetime.html#strftime-and-strptime-format-codes
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
        logger.error(
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
    line = re.sub(r'[\,\.]', '', str_value)

    return line
