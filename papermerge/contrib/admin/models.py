import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class LogEntry(models.Model):
    """
    LogEntry visible on left side panel.
    Each user can see his/her logs.
    Superuser can see everybody's log.

    LogEntries are very useful to gets insights into OCRs and Automates
    activity. In general to see what is happening in the Papermerge system.
    """

    LEVELS = (
        (logging.DEBUG, _("Debug")),
        (logging.INFO, _("Info")),
        (logging.WARNING, _("Warning")),
        (logging.ERROR, _("Error")),
        (logging.CRITICAL, _("Critical")),
    )

    message = models.TextField()
    level = models.PositiveIntegerField(
        choices=LEVELS,
        default=logging.INFO
    )

    action_time = models.DateTimeField(
        _('action time'),
        default=timezone.now,
        editable=False,
    )

    user = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')
        ordering = ('-action_time',)

