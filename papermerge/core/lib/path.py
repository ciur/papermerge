
import re
import os

SUPPORTED_EXTENTIONS = re.compile(".*(jpeg|jpg|png|tiff|pdf)$", re.IGNORECASE)


def filter_by_extention(
    names_list,
    compiled_reg_expr=SUPPORTED_EXTENTIONS
):
    """
    input:
        names_list
            is a list/tubple with string entries.
        compiled_reg_expr
            compiled regular expression pattern for file extentions to filter.
            Only file names of whom extentions match compiled_reg_expr
            will stay in returned list

    returns another list containing only entries with extention
    matching given pattern.
    """
    result = []

    for name in names_list:
        root, ext = os.path.splitext(name)
        if compiled_reg_expr.match(ext):
            result.append(name)

    return result
