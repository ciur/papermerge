from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from knox.models import AuthToken
from papermerge.core.models import User


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'is_superuser',
            'is_staff',
            'is_active',
            'last_login',
        )


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
