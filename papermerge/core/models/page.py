import logging
import os

from django.db import models
from mglib.path import PagePath
from papermerge.core.storage import default_storage
from papermerge.search import index
from papermerge.search.queryset import SearchableQuerySetMixin

from .diff import Diff
from .document import Document
from .kvstore import KVCompPage, KVPage, KVStorePage

logger = logging.getLogger(__name__)


class PageQuerySet(SearchableQuerySetMixin, models.QuerySet):
    pass


class Page(models.Model, index.Indexed):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='pages'
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

    image = models.CharField(
        max_length=1024,
        default=''
    )

    objects = PageQuerySet.as_manager()

    def to_dict(self):

        item = {}
        item['id'] = self.id
        item['number'] = self.number
        item['kvstore'] = [item.to_dict() for item in self.kv.all()]

        return item

    @property
    def kv(self):
        return KVPage(instance=self)

    @property
    def kvcomp(self):
        return KVCompPage(instance=self)

    def _apply_diff_add(self, diff):

        self.kv.apply_additions(
            [
                {
                    'kv_inherited': True,
                    'key': _model.key,
                    'kv_format': _model.kv_format,
                    'kv_type': _model.kv_type
                }
                for _model in diff
            ]
        )

    def _apply_diff_update(self, diff, attr_updates):
        updates = [{
            'kv_inherited': True,
            'key': _model.key,
            'kv_format': _model.kv_format,
            'kv_type': _model.kv_type,
            'id': _model.id
        } for _model in diff]

        updates.extend(attr_updates)

        self.kv.apply_updates(updates)

    def _apply_diff_delete(self, diff):
        pass

    def apply_diff(self, diffs_list, attr_updates):

        for diff in diffs_list:
            if diff.is_add():
                self._apply_diff_add(diff)
            elif diff.is_update():
                self._apply_diff_update(diff, attr_updates)
            elif diff.is_delete():
                self._apply_diff_delete(diff)
            elif diff.is_replace():
                # not applicable to page model
                # replace is used in access permissions
                # propagation
                pass
            else:
                raise ValueError(
                    f"Unexpected diff {diff} type"
                )

    def inherit_kv_from(self, document):
        instances_set = []

        for kvstore in document.kv.all():
            instances_set.append(
                KVStorePage(
                    key=kvstore.key,
                    kv_format=kvstore.kv_format,
                    kv_type=kvstore.kv_type,
                    value=kvstore.value,
                    kv_inherited=True,
                    page=self
                )
            )

        diff = Diff(
            operation=Diff.ADD,
            instances_set=instances_set
        )

        self.propagate_changes(
            diffs_set=[diff],
        )

    def propagate_changes(
        self,
        diffs_set,
        apply_to_self=None,
        attr_updates=[]
    ):
        """
        apply_to_self argument does not make sense here.
        apply_to_self argument is here to make this function
        similar to node.propagate_changes.
        """
        self.apply_diff(
            diffs_list=diffs_set,
            attr_updates=attr_updates
        )

    @property
    def is_last(self):
        return self.number == self.page_count

    @property
    def is_first(self):
        return self.number == 1

    def path(self, version=None):

        return PagePath(
            document_path=self.document.path(version=version),
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

    @property
    def txt_url(self):

        result = PagePath(
            document_path=self.document.path(),
            page_num=self.number,
            page_count=self.page_count
        )

        return result.txt_url()

    @property
    def txt_exists(self):

        result = PagePath(
            document_path=self.document.path(),
            page_num=self.number,
            page_count=self.page_count
        )

        return result.txt_exists()

    def norm(self):
        """shortcut normalization method"""
        self.normalize_doc_title()
        self.normalize_folder_title()
        self.normalize_breadcrump()
        self.normalize_text()
        self.normalize_lang()

    def normalize_doc_title(self):
        """
        Save containing document's title
        """
        self.norm_doc_title = self.document.title
        self.save()

    def normalize_folder_title(self):
        """
        Save direct parent folder (containing folder) title
        """
        if self.document.parent:
            self.norm_folder_title = self.document.parent.title
            self.save()

    def normalize_breadcrump(self):
        pass

    def normalize_text(self):
        pass

    def normalize_lang(self):
        pass

    class Meta:
        # Guarantees that
        # doc.pages.all() will return pages ordered by number.
        # test by
        # test_page.TestPage.test_pages_all_returns_pages_ordered
        ordering = ['number']
