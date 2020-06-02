import logging
import os

from django.db import models
from mglib.path import PagePath
from papermerge.core.models import Document
from papermerge.core.storage import default_storage
from papermerge.search import index
from papermerge.search.queryset import SearchableQuerySetMixin

logger = logging.getLogger(__name__)


class PageQuerySet(SearchableQuerySetMixin, models.QuerySet):
    pass


class Page(models.Model, index.Indexed):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE
    )
    user = models.ForeignKey('User', models.CASCADE)

    number = models.IntegerField(default=1)
    page_count = models.IntegerField(default=1)

    text = models.TextField(default='')

    # inherited/normalized title from parent document
    norm_doc_title = models.CharField(
        max_length=200,
        default=''
    )

    # inherited/normalized title of immediate parent folder
    norm_folder_title = models.CharField(
        max_length=200,
        default=''
    )

    # normalized space delimited path (by folder title) of parent folder
    norm_breadcrump = models.CharField(
        max_length=1024,
        default=''
    )

    # text from all pages of the document
    norm_text = models.TextField(default='')

    # hm, this one should be norm_lang as well
    lang = models.CharField(
        max_length=8,
        blank=False,
        null=False,
        default='deu'
    )

    search_fields = [
        index.SearchField('norm_doc_title', partial_match=True, boost=3),
        index.SearchField('norm_folder_title', partial_match=True),
        index.SearchField('norm_breadcrump', partial_match=True),
        index.SearchField('norm_text', partial_match=True, boost=1),
        index.SearchField('text', partial_match=True, boost=2),
        index.FilterField('lang')
    ]

    objects = PageQuerySet.as_manager()

    @property
    def is_last(self):
        return self.number == self.page_count

    @property
    def is_first(self):
        return self.number == 1

    @property
    def path(self):
        return PagePath(
            document_ep=self.document.doc_ep,
            page_num=self.number,
            page_count=self.page_count
        )

    def update_text_field(self):
        """Update text field from associated .txt file.

        Returns non-empty text string value if .txt file was found.
        If file was not found - will return an empty string.
        """
        text = ''
        url = default_storage.abspath(self.txt_url)

        if not os.path.exists(url):
            logger.debug(
                f"Missing page txt {url}."
            )
            return

        with open(url) as file_handle:
            self.text = file_handle.read()
            self.save()
            logger.debug(
                f"text saved. len(page.text)=={len(self.text)}"
            )
            text = self.text

        return text

    image = models.CharField(
        max_length=1024,
        default=''
    )

    @property
    def txt_url(self):

        result = PagePath(
            document_path=self.document.path,
            page_num=self.number,
            page_count=self.page_count
        )

        return result.txt_url()

    @property
    def txt_exists(self):

        result = PagePath(
            document_path=self.document.path,
            page_num=self.number,
            page_count=self.page_count
        )

        return result.txt_exists()

    def norm(self):
        """normalization method"""
        pass
