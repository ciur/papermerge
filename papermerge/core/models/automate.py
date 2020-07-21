from django.db import models
from django.utils.translation import ugettext_lazy as _


class Automate(models.Model):

    """
    Automates:
        * moving of documents into destination folder
        * extraction of metadata
    """

    MATCH_ANY = 1
    MATCH_ALL = 2
    MATCH_LITERAL = 3
    MATCH_REGEX = 4
    MATCH_FUZZY = 5

    MATCHING_ALGORITHMS = (
        (MATCH_ANY, _("Any")),
        (MATCH_ALL, _("All")),
        (MATCH_LITERAL, _("Literal")),
        (MATCH_REGEX, _("Regular Expression")),
    )

    name = models.CharField(
        max_length=128,
        unique=True
    )

    # text to match
    match = models.CharField(
        max_length=256,
        blank=True
    )

    matching_algorithm = models.PositiveIntegerField(
        choices=MATCHING_ALGORITHMS,
        default=MATCH_ANY,
    )

    # shoud be matching case_sensitive? i.e. uppercase == lowercase
    is_case_sensitive = models.BooleanField(
        default=True
    )

    # name of plugin used to extract metadata, if any.
    # Must match metadata associated with dst_folder
    plugin_name = models.CharField(
        max_length=256,
        blank=True,
        choices=(),
        default=None,
    )

    # Must match correct plugin (in case you wish automate metadta extract)
    dst_folder = models.ForeignKey(
        'Folder',
        on_delete=models.DO_NOTHING
    )

    # Should this page be cutted and pasted as separate document?
    # Very useful in case of bulk receipts scans
    extract_page = models.BooleanField(
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

