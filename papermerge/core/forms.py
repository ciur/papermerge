from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.forms.widgets import (
    TextInput,
    EmailInput,
    ChoiceWidget
)

from knox.models import AuthToken

from papermerge.core.models import User, Automate


class AutomateForm(forms.ModelForm):

    class Meta:
        model = Automate

        fields = (
            'name',
            'match',
            'matching_algorithm',
            'is_case_sensitive',
            'plugin_name',
            'dst_folder',
            'extract_page'
        )

    def __init__(self, *args, **kwargs):
        plugin_choices = kwargs.pop('plugin_choices', ())

        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if isinstance(
                visible.field.widget,
                (TextInput, EmailInput, ChoiceWidget)
            ):
                visible.field.widget.attrs['class'] = 'form-control'

        # dynamically populate plugin choices
        self.fields['plugin_name'].choices = plugin_choices


class UserFormWithoutPassword(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'groups',
            'is_superuser',
            'is_staff',
            'is_active',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(
                visible.field.widget,
                (TextInput, EmailInput, ChoiceWidget)
            ):
                visible.field.widget.attrs['class'] = 'form-control'


class UserFormWithPassword(UserFormWithoutPassword):

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        strip=True,
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        strip=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'groups',
            'is_superuser',
            'is_staff',
            'is_active',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(
                visible.field.widget,
                (TextInput, EmailInput, ChoiceWidget)
            ):
                visible.field.widget.attrs['class'] = 'form-control'

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        try:
            validate_password(password2, self.instance)
        except forms.ValidationError as error:
            self.add_error('password2', error)
        return password2


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = (
            'name',
        )


class AuthTokenForm(forms.ModelForm):
    """
    Let user choose number of hours until token expires
    """
    hours = forms.IntegerField(
        required=True,
        initial=4464,  # ~ 6 months
        help_text=_(
            "Number of hours this token will be valid (4464 hours ~ 6 months)"
        ),
    )

    class Meta:
        model = AuthToken
        fields = ('hours',)
