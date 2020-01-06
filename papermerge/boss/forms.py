from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.forms import AdminAuthenticationForm
from papermerge.core.forms import PasswordInput


class BossAuthenticationForm(AdminAuthenticationForm):
    """
    A custom authentication form used in the admin app.
    """
    error_messages = {
        'invalid_login': _(
            "Please enter the correct %(username)s and password for your "
            "account. Note that both fields may be case-sensitive."
        ),
    }

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput,
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )
