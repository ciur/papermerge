from django import forms
from django.forms.widgets import (
    TextInput,
    ChoiceWidget,
    Textarea
)

from papermerge.core.models import Tag

from .models import (
    LogEntry,
)


class LogEntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if isinstance(
                visible.field.widget,
                (TextInput, Textarea, ChoiceWidget)
            ):
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = LogEntry
        fields = (
            'message',
            'level',
        )

class TagForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if isinstance(
                visible.field.widget,
                (TextInput, Textarea, ChoiceWidget)
            ):
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Tag
        fields = (
            'name',
            'fg_color',
            'bg_color',
            'description'
        )
        widgets = {
            'fg_color': TextInput(attrs={'type': 'color'}),
            'bg_color': TextInput(attrs={'type': 'color'}),
        }

