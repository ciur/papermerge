import re


class ExtractIds:
    EXTR_DOC_IDS = re.compile('document_(?P<id>\d+)')
    EXTR_FOLDER_IDS = re.compile('folder_(?P<id>\d+)')

    def extract_ids(regexp, fmt_list):
        """
        Returns a list of ids extracted from all matched members of given as
        input formated list.
        """

        if not isinstance(regexp, re._pattern_type):
            raise ValueError("Expecting first arg to be a regexp")

        ret_ids = []

        for mem in fmt_list:
            matched_obj = re.match(regexp, mem)
            if not matched_obj:
                continue
            try:
                matched_obj['id']
            except Exception:
                continue

            if matched_obj['id']:
                ret_ids.append(
                    matched_obj['id']
                )

        return ret_ids
