from django import forms
from django.forms import widgets

from django.contrib.auth.forms import (
    AdminPasswordChangeForm
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import (
    password_validation
)

from papermerge.core.models import (
    Document,
    Folder,
    Subscription,
    UserProfile
)


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
            'language',
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
            'language', 'page_count'
        ]


class FolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = [
            'title',
        ]
        exclude = ['user', 'keywords', 'color']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'sftp_password1',
            'sftp_password2'
        ]
        widgets = {
            'sftp_password1': PasswordInput(),
            'sftp_password2': PasswordInput(),
        }
        labels = {
            'sftp_password1': 'Password',
            'sftp_password2': 'Password (again)'
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('email', )
