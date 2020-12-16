from functools import reduce
from itertools import groupby

from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    Group,
    Permission
)
from django.contrib.auth.password_validation import validate_password
from django.forms.widgets import (
    TextInput,
    ChoiceWidget,
    EmailInput,
)

from mptt.forms import TreeNodeChoiceField
from knox.models import AuthToken

from papermerge.core.models import (
    Tag,
    User,
    Role,
    Automate,
    Folder,
    Access
)

from .models import (
    LogEntry,
)


def _papermerge_permissions():
    """
    Returns a queryset of permissions which makes sense
    to display. For example it does not make sense to
    show permissions for BaseTreeNode model - user is not
    even aware of what is it (and should not be).
    """
    qs = Permission.objects.filter(
        content_type__model__in=[
            "user",
            "role",
            "group",
            "authtoken",
            "session",
            "document",
            "folder",
            "userpreferencemodel",
            "automate"
        ]
    )

    return qs.all()


class ControlForm(forms.ModelForm):
    """
    Adds to following widgets css class 'form-control':
        * TextInput
        * EmailInput
        * ChoiceWidget
        * TreeNodeChoiceField

    Additional, for ChoiceWidget (<select> tag) appends 'custom-select'
    css class
    """

    def __init__(self, *args, **kwargs):
        # get rid of custom arg
        kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if isinstance(
                visible.field.widget,
                (TextInput, EmailInput, ChoiceWidget, TreeNodeChoiceField)
            ):
                visible.field.widget.attrs['class'] = 'form-control'

            if isinstance(visible.field.widget, ChoiceWidget):
                visible.field.widget.attrs['class'] += ' custom-select '


class LogEntryForm(ControlForm):

    class Meta:
        model = LogEntry
        fields = (
            'message',
            'level',
        )


class TagForm(ControlForm):

    class Meta:
        model = Tag
        fields = (
            'name',
            'pinned',
            'fg_color',
            'bg_color',
            'description'
        )
        widgets = {
            'fg_color': TextInput(attrs={'type': 'color'}),
            'bg_color': TextInput(attrs={'type': 'color'}),
        }


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    # Adds a checkbox (group checkbox) and designated it with 'multi-target'
    # css class
    template_name = "admin/widgets/checkbox_select.html"


class GroupedModelChoiceIterator(forms.models.ModelChoiceIterator):

    def _key_func(self, obj):
        return reduce(getattr, self.field.group_by.split('__'), obj)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)

        object_list = sorted(self.queryset.all(), key=self._key_func)

        for group, choices in groupby(object_list, key=self._key_func):
            if group is not None:
                yield (
                    self.field.group_label(group),
                    [self.choice(c) for c in choices]
                )


class CustomPermissionChoiceField(forms.ModelMultipleChoiceField):
    """
    Provides great UX for Permission selection
    1. Groups permissions by model
    2. Provides human friendly labels
    """

    def __init__(
        self,
        group_by,
        sort_choices_by=None,
        *args,
        **kwargs
    ):
        # use custom checkbox multiple select
        # The point is that custom widget adds an additional
        # checkbox (group checkbox) and designated it with 'multi-target'
        # css class
        kwargs['widget'] = CustomCheckboxSelectMultiple
        super().__init__(*args, **kwargs)

        self.group_by = group_by
        self.group_label = lambda group: group.capitalize()

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)

    choices = property(
        _get_choices,
        forms.ModelMultipleChoiceField._set_choices
    )

    def label_from_instance(self, member):
        # Human friendly labels
        return f"{member.name}"


class RoleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # get rid of custom arg
        kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

    class Meta:
        model = Role
        fields = (
            'name',
            'permissions'
        )

    permissions = CustomPermissionChoiceField(
        # display only permissions which are part of sipadmin app
        queryset=_papermerge_permissions(),
        group_by='content_type__model',
    )


class AutomateForm(ControlForm):

    class Meta:
        model = Automate

        fields = (
            'name',
            'match',
            'matching_algorithm',
            'is_case_sensitive',
            'tags',
            'dst_folder',
        )
        field_classes = {
            'dst_folder': TreeNodeChoiceField,
        }

    def __init__(self, *args, **kwargs):
        # first get rid of custom arg
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)

        self.fields['dst_folder'].queryset = Folder.objects.none()

        if instance:
            user = instance.user

        if user:
            # Provide user a choice of all folder he/she has
            # WRITE access to. User might have access to folder he is not
            # the owner of.
            # Exclude folder - inbox
            all_folders = Folder.objects.exclude(
                title=Folder.INBOX_NAME
            )

            folder_choice_ids = []

            for folder in all_folders:
                if user.has_perm(Access.PERM_WRITE, folder):
                    folder_choice_ids.append(folder.id)

            self.fields['dst_folder'].queryset = Folder.objects.filter(
                id__in=folder_choice_ids
            )


class AdvancedSearchForm(forms.Form):
    folder = TreeNodeChoiceField(
        queryset=None,
        required=False
    )
    text = forms.CharField()
    tags = forms.CharField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:
            all_folders = Folder.objects.exclude(
                title=Folder.INBOX_NAME
            )
            folder_choice_ids = []

            nodes_perms = user.get_perms_dict(
                all_folders, Access.ALL_PERMS
            )

            for folder in all_folders:
                if nodes_perms[folder.id].get(Access.PERM_READ, False):
                    folder_choice_ids.append(folder.id)

            self.fields['folder'].queryset = Folder.objects.filter(
                id__in=folder_choice_ids
            )


class UserFormWithoutPassword(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'groups',
            'role',
            'is_superuser',
            'is_active',
        )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        # get rid of custom arg
        kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        # don't use neither form-control nor 'custom-select' css classes here
        self.fields['groups'].widget.attrs['class'] = ' '


class UserChangePasswordForm(forms.Form):

    password1 = forms.CharField(
        widget=forms.PasswordInput(), label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(), label="Confirm Password"
    )

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error(
                "password1",
                "Both fields should contain same password"
            )
            self.add_error(
                "password2",
                "Both fields should contain same password"
            )

        if len(password1) > 0 and len(password1) < 6:
            self.add_error(
                "password1",
                "Password must be at least 6 characters long"
            )
            self.add_error(
                "password2",
                "Password must be at least 6 characters long"
            )


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
            'role',
            'is_superuser',
            'is_active',
        )

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

    def __init__(self, *args, **kwargs):
        # first get rid of custom arg
        kwargs.pop('user', None)

        super().__init__(*args, **kwargs)


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
