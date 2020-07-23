import logging
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .document import Document


logger = logging.getLogger(__name__)


class Automate(models.Model):

    """
    Automates:
        * moving of documents into destination folder
        * extraction of metadata
    """

    # any match - looks for any occurrence of any word
    # provided in the document
    MATCH_ANY = 1
    # all match - looks for all occurrences of all words
    # provided in the document (order does not matter)
    MATCH_ALL = 2
    # literal match means that the text you enter must appear in
    # the document exactly as you've entered it
    MATCH_LITERAL = 3
    # reg exp match
    MATCH_REGEX = 4

    MATCHING_ALGORITHMS = (
        (MATCH_ANY, _("Any")),
        (MATCH_ALL, _("All")),
        (MATCH_LITERAL, _("Literal")),
        (MATCH_REGEX, _("Regular Expression")),
    )

    name = models.CharField(
        _('Name'),
        max_length=128,
        unique=True
    )

    # text to match
    match = models.CharField(
        _('Match'),
        max_length=256,
        blank=True
    )

    matching_algorithm = models.PositiveIntegerField(
        _('Matching Algorithm'),
        choices=MATCHING_ALGORITHMS,
        default=MATCH_ANY,
    )

    # shoud be matching case_sensitive? i.e. uppercase == lowercase
    is_case_sensitive = models.BooleanField(
        _('Is case sensitive'),
        default=True
    )

    # name of plugin used to extract metadata, if any.
    # Must match metadata associated with dst_folder
    plugin_name = models.CharField(
        _('Plugin Name'),
        max_length=256,
        blank=True,
        null=True,
        choices=(),
        default=None,
    )

    # Must match correct plugin (in case you wish automate metadta extract)
    dst_folder = models.ForeignKey(
        'Folder',
        on_delete=models.DO_NOTHING,
        verbose_name=_('Destination Folder')
    )

    # Should this page be cutted and pasted as separate document?
    # Very useful in case of bulk receipts scans
    extract_page = models.BooleanField(
        _('Extract Page'),
        default=False
    )

    user = models.ForeignKey(
        'User',
        models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def is_a_match(self, hocr):
        # Check that match is not empty
        if self.match.strip() == "":
            return False

        search_kwargs = {}
        if self.is_case_sensitive:
            search_kwargs = {"flags": re.IGNORECASE}

        if self.matching_algorithm == Automate.MATCH_ANY:
            return self._match_any(hocr, search_kwargs)

        if self.matching_algorithm == Automate.MATCH_ALL:
            return self._match_all(hocr, search_kwargs)

        if self.matching_algorithm == Automate.MATCH_LITERAL:
            return self._match_literal(hocr, search_kwargs)

        if self.matching_algorithm == Automate.MATCH_REGEX:
            return self._match_regexp(hocr, search_kwargs)

        return False

    def move_to(self, document, dst_folder):
        document.refresh_from_db()
        dst_folder.refresh_from_db()

        if document and dst_folder:
            Document.objects.move_node(
                document, dst_folder
            )

    def apply(
        self,
        document,
        page_num,
        hocr,
        plugin=None
    ):
        new_document = None
        logger.debug("automate.Apply begin")

        if document.page_count == 1:
            # i.e if this is last page
            # move entire document to the destination folder
            self.move_to(
                document,
                self.dst_folder
            )
        elif self.extract_page:
            # dealing with case when this is not
            # last page of the document AND extraction
            # of the page is wanted.
            if self.dst_folder != document.parent:
                new_document = Document.paste_pages(
                    user=document.user,
                    parent_id=self.dst_folder.id,
                    doc_pages={
                        document.id: [page_num]
                    }

                )

        if plugin:
            logger.debug("Plugin is provided, extracting hocr")
            metadata = plugin.extract(hocr)
            logger.debug(
                f"Metadata Extracted with Automate={metadata}"
            )
            doc = new_document if new_document else document

            doc.assign_kv_values(
                metadata['simple_keys']
            )

    def _match_any(self, hocr, search_kwargs):

        for word in self._split_match():
            regexp = r"\b{}\b".format(word)
            if re.search(regexp, hocr, **search_kwargs):
                return True

        return False

    def _match_all(self, hocr, search_kwargs):

        for word in self._split_match():
            regexp = r"\b{}\b".format(word)
            search_result = re.search(
                regexp,
                hocr,
                **search_kwargs
            )
            if not search_result:
                return False

        return True

    def _match_literal(self, hocr, search_kwargs):
        """
        Simplest match - literal match  i.e.
        exact match of the given word or string.
        """
        regexp = r"\b{}\b".format(self.match)
        result = re.search(regexp, hocr, **search_kwargs)
        return bool(result)

    def _match_regexp(self, hocr, search_kwargs):
        regexp = re.compile(self.match, **search_kwargs)

        result = re.search(regexp, hocr)

        return bool(result)

    def _split_match(self):
        """
        Splits the match to individual keywords, getting rid of unnecessary
        spaces and grouping quoted words together.
        Example:
          '  some random  words "with   quotes  " and   spaces'
            ==>
          ["some", "random", "words", "with+quotes", "and", "spaces"]
        """
        findterms = re.compile(r'"([^"]+)"|(\S+)').findall
        normspace = re.compile(r"\s+").sub
        return [
            normspace(" ", (t[0] or t[1]).strip()).replace(" ", r"\s+")
            for t in findterms(self.match)
        ]
