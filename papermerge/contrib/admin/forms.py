from django import forms

from .models import LogEntry


class LogEntryForm(forms.ModelForm):

    class Meta:
        model = LogEntry
        fields = (
            'message',
            'level'
        )

