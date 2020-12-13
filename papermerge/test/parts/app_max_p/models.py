from django.core.exceptions import ValidationError

from papermerge.core.models import AbstractDocument


class Document(AbstractDocument):
    """
    This document part a validation of maximum number of pages per document.
    """

    MAX_PAGES = 100

    def clean(self):
        if self.get_pagecount() > Document.MAX_PAGES:
            raise ValidationError({
                "page_count": f"Max pages {Document.MAX_PAGES} allowed"
            })
