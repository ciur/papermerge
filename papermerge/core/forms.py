from django import forms
from django.forms import widgets

from django.contrib.auth.forms import (
    AdminPasswordChangeForm
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import (
    password_validation
)

from papermerge.core.models import (Document, Folder)


class TailedInput(widgets.Input):
    input_type = 'text'
    template_name = 'boss/forms/widgets/tailed_input.html'

    def __init__(self, attrs=None, render_value=False):
        super().__init__(attrs)
        self.render_value = render_value

    def get_context(self, name, value, attrs):
        if not self.render_value:
            value = None
        return super().get_context(name, value, attrs)


class PasswordInput(widgets.Input):
    input_type = 'password'
    template_name = 'boss/forms/widgets/password.html'

    def __init__(self, attrs=None, render_value=False):
        super().__init__(attrs)
        self.render_value = render_value

    def get_context(self, name, value, attrs):
        if not self.render_value:
            value = None
        return super().get_context(name, value, attrs)


class DgPasswordChangeForm(AdminPasswordChangeForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=PasswordInput(attrs={'autofocus': True}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document

        fields = [
            'title',
            'lang',
            'notes',
        ]


class PageForm(forms.ModelForm):

    image = forms.CharField(
        required=False,
        widget=forms.TextInput,
        max_length=1024
    )
    number = forms.IntegerField(disabled=True, widget=forms.TextInput)

    class Meta:
        exclude = [
            'user', 'height', 'text_deu', 'text_eng', 'text',
            'lang', 'page_count'
        ]


class FolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = [
            'title',
        ]
        exclude = ['user', 'keywords', 'color']


class AuthTokenForm(forms.ModelForm):
    """
    Let user choose number of hours until token expires
    """
    hours = forms.IntegerField(
        required=True,
        initial=4464,  # ~ 6 months
        help_text=_(
            "Number of hours this token will be valid (since its creation)"
        ),
    )

    class Meta:
        fields = ('hours',)
