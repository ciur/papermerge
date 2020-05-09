from django.db import models
from django.contrib.postgres.search import SearchVectorField

from papermerge.core.models import (Document, User)


class Page(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, models.CASCADE)

    number = models.IntegerField(default=1)
    page_count = models.IntegerField(default=1)

    text = models.TextField(default='')

    lang = models.CharField(
        max_length=8,
        blank=False,
        null=False,
        default='deu'
    )
    # Obsolete columns. Replaced by text_fts.
    text_deu = SearchVectorField(null=True)
    text_eng = SearchVectorField(null=True)

    # Replaced text_deu and text_eng
    text_fts = SearchVectorField(null=True)

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
        logger.debug(f"Checking {self.txt_url}")

        if not self.txt_exists:
            logger.debug(
                f"Missing page txt {self.txt_url}."
            )
            return
        else:
            logger.debug(f"Page txt {self.txt_url} exists.")

        with open(self.txt_url) as file_handle:
            self.text = file_handle.read()
            self.save()
            logger.debug(
                f"text saved. len(page.text)=={len(self.text)}"
            )
            text = self.text
            logger.info(
                f"document_log "
                f" username={self.user.username}"
                f" doc_id={self.document.id}"
                f" page_num={self.number}"
                f" text_len={len(self.text.strip())}"
            )

        return text

    image = models.CharField(
        max_length=1024,
        default=''
    )

    @property
    def txt_url(self):

        result = PagePath(
            document_ep=self.document.path,
            page_num=self.number,
            page_count=self.page_count
        )

        return result.txt_url()

    @property
    def txt_exists(self):

        result = PagePath(
            document_ep=self.document.doc_ep,
            page_num=self.number,
            page_count=self.page_count
        )

        return result.txt_exists()