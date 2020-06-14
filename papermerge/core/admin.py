import logging
from datetime import timedelta

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter, options
from django.contrib.admin.actions import delete_selected
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ORDER_VAR
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.forms import inlineformset_factory
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from dynamic_preferences.admin import SectionFilter
from dynamic_preferences.settings import preferences_settings
from dynamic_preferences.users.forms import UserSinglePreferenceForm
from dynamic_preferences.users.models import UserPreferenceModel
from knox.models import AuthToken
from papermerge.boss import admin as bs_admin
from papermerge.boss import options as bs_options
from papermerge.boss import widgets as boss_widgets
from papermerge.boss.views.main import ChangeListBoss
from papermerge.core import forms, models
from papermerge.core.preview import PreviewUrlsHandover
from papermerge.search.backends import get_search_backend
from pmworker import lang_human_name
from polymorphic_tree.admin import (PolymorphicMPTTChildModelAdmin,
                                    PolymorphicMPTTParentModelAdmin)

User = get_user_model()

logger = logging.getLogger(__name__)


class PageInline(options.StackedInline):

    template = 'boss/edit_inline/stacked_pages.html'

    model = models.Page
    form = forms.PageForm
    formset = inlineformset_factory(
        models.Document,
        models.Page,
        form=forms.PageForm,
        extra=0,
    )

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('documents.delete', obj)

    def has_add_permission(self, request, obj=None):
        # User cannot add pages his own... he actually can do that,
        # but not buy means of usual django forms.
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def get_extra(self, request, obj=None, **kwargs):
        """Hook for customizing the number of extra inline forms."""

        # When displaying document pages , there is no need to
        # add extra forms. User cannot add/change them anyway
        return 0


# The common admin functionality for all derived models:

class BaseChildAdmin(
    bs_options.BaseModelBoss,
    PolymorphicMPTTChildModelAdmin
):
    GENERAL_FIELDSET = (None, {
        'fields': ('parent', 'title'),
    })

    base_model = models.BaseTreeNode
    base_fieldsets = (
        GENERAL_FIELDSET,
    )


class FolderNodeAdmin(BaseChildAdmin):
    list_display = ('title',)
    exclude = ('user',)
    fields = ('title', 'parent')

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        parent_id = request.GET.get('p_id', None)

        # this is repetetive, refactor it!
        qs = models.BaseTreeNode.objects.filter(user=request.user).all()

        if parent_id:
            parent_id = int(parent_id)
        if parent_id and parent_id in list(qs.values_list('id', flat=True)):
            try:
                models.BaseTreeNode.objects.get(id=parent_id)
                initial['parent'] = parent_id
            except models.BaseTreeNode.DoesNotExist:
                raise

        return initial

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):

        if db_field.name == 'node_permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')

            kwargs['queryset'] = kwargs['queryset'].filter(
                codename__in=('vml_change',)
            )
        form_field = super().formfield_for_manytomany(
            db_field,
            request=request,
            **kwargs
        )

        if db_field.name == 'node_permissions':
            form_field.widget = boss_widgets.PermissionsSelectMultiple(
                db_field.verbose_name,
                db_field.name in self.filter_vertical
            )

        return form_field

    def changeform_view(
        self,
        request,
        object_id=None,
        form_url='',
        extra_context=None
    ):

        extra_context = {}
        parent_id = request.GET.get('p_id', None)
        parent_obj = None

        qs = models.BaseTreeNode.objects.filter(user=request.user).all()

        if parent_id:
            parent_id = int(parent_id)
        if parent_id and parent_id in list(qs.values_list('id', flat=True)):
            parent_obj = models.BaseTreeNode.objects.get(id=parent_id)
            extra_context['object'] = parent_obj

        return super().changeform_view(
            request,
            object_id=object_id,
            form_url=form_url,
            extra_context=extra_context
        )

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm("vml_documents")

    def has_add_permission(self, request, obj=None):
        return request.user.has_perm("vml_documents")

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('documents.delete')


class DocumentNodeAdmin(BaseChildAdmin):
    list_display = (
        'title',
        'size',
    )

    # By using these `base_...` attributes instead of the regular
    # ModelAdmin `form` and `fieldsets`, the additional fields of the
    # child models are automatically added to the admin form.
    base_form = forms.DocumentForm

    inlines = (
        PageInline,
    )

    exclude = (
        'size', 'text', 'user',
        'title_deu', 'title_eng', 'title_fts',
        'ancestors_deu', 'ancestors_eng', 'ancestors_fts',
        'text_eng', 'text_deu', 'text_fts',
        'digest', 'file_orig', 'file_name',
        'node_permissions',
        'page_count', 'groups', 'version',
    )

    search_fields = ('title', 'text')

    def get_preview_urls(self, object_id):
        doc = models.Document.objects.get(id=object_id)

        urls = PreviewUrlsHandover(
            document_id=doc.id, page_count=doc.page_count
        )

        return list(urls)

    def get_parent_url(self, object_id):
        doc = models.Document.objects.get(id=object_id)
        if doc.parent:
            return reverse(
                'boss:core_basetreenode_changelist_obj',
                args=(doc.parent.id, ),
            )

        return reverse(
            'boss:core_basetreenode_changelist'
        )

    def get_default_height(self):
        return settings.PDFTOPPM_DEFAULT_HEIGHT

    def change_view(
            self,
            request,
            object_id,
            form_url='',
            extra_context=None
    ):
        # Changeform view
        # where are document viewer, with page thumbnails list,
        # left/right sidebars
        extra_context = extra_context or {}
        doc = models.Document.objects.get(id=object_id)
        extra_context['parent_url'] = self.get_parent_url(object_id)
        extra_context['title'] = doc.title
        extra_context['preview_urls'] = self.get_preview_urls(object_id)
        extra_context['default_height'] = self.get_default_height()
        extra_context['pages'] = doc.pages.order_by('number')

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return request.user.has_perm("vml_documents")

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('documents.delete', obj)


# Snatched this one from
# polymorphic_tree/admin/parentadmin
# just ty change title!
class NodeTypeListFilter(SimpleListFilter):
    parameter_name = 'ct_id'
    title = _('Type')

    def lookups(self, request, model_admin):
        return model_admin.get_child_type_choices(request, 'change')

    # Whoops: Django 1.6 didn't rename this one!
    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(polymorphic_ctype_id=self.value())
        return queryset


class TreeNodeParentAdmin(
    bs_options.BaseModelBoss,
    PolymorphicMPTTParentModelAdmin
):
    """
    From django-polymorphic docs:
        https://django-polymorphic.readthedocs.io/en/stable/admin.html#setup

    Both the parent model and child model need to have a ModelAdmin class.
    The shared base model should use the PolymorphicParentModelAdmin
    as base class.

        * base_model should be set
        * child_models or get_child_models() should return an iterable
        of Model classes.

    The admin class for every child model should inherit from
    PolymorphicChildModelAdmin. base_model should be set.

    Although the child models are registered too,
    they won’t be shown in the admin index page.
    This only happens when show_in_index is set to True.

    The parent admin is only used for the list display of models,
    and for the edit/delete view of non-subclassed models.
    All other model types are redirected to the edit/delete/history view
    of the child model admin.
    Hence, the fieldset configuration should be placed on the child admin.
    """
    base_model = models.BaseTreeNode
    child_models = (
        models.Document,
        # custom admin allows custom edit/delete view.
        models.Folder
    )

    def owner(self, obj):
        return obj.user.username

    list_display = (
        'title_with_class',
        'created_at',
    )

    ordering = ('-polymorphic_ctype', '-created_at')

    list_per_page = 20

    list_filter = (NodeTypeListFilter, )

    #  date_hierarchy = 'created_at'

    search_fields = [
        'folder___title',
        'document__title',
        'document__text'
    ]

    def get_ordering(self, request):
        """
        if ordering param is not present, read last_saved_order
        cookie and return fields accordingly.
        """
        local_map = {
            "1": "title",
            "-1": "-title",
            "2": "created_at",
            "-2": "-created_at",
            "3": "polymorphic_ctype",
            "-3": "-polymorphic_ctype",
        }
        if request.method != 'GET':
            return self.ordering

        if request.GET.get(ORDER_VAR, False):
            return self.ordering

        last_sort = request.COOKIES.get('save_last_sort', False)

        if last_sort in local_map.keys():
            # ordering must be a list
            return ('-polymorphic_ctype', local_map[last_sort],)

        return self.ordering



    def delete_selected_tree(self, modeladmin, request, queryset):
        """
        Deletes multiple instances and makes sure the MPTT fields get
        recalculated properly. (Because merely doing a bulk delete doesn't
        trigger the post_delete hooks.)
        """
        # If this is True, the confirmation page has been displayed
        if request.POST:
            n = 0
            with queryset.model._tree_manager.delay_mptt_updates():
                for obj in queryset:
                    if self.has_delete_permission(request, obj):
                        obj.delete()
                        n += 1
                        obj_display = force_text(obj)
                        self.log_deletion(request, obj, obj_display)
            self.message_user(
                request,
                _('Successfully deleted %(count)d items.') % {'count': n})
            # Return None to display the change list page again
            return None
        else:
            # (ab)using the built-in action to display the confirmation page
            return delete_selected(self, request, queryset)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions is not None and 'delete_selected' in actions:
            actions['delete_selected'] = (
                self.delete_selected_tree,
                'delete_selected',
                _('Delete selected %(verbose_name_plural)s'))
        return actions

    def get_qs_from_raw_sql(self, request, search_term):
        backend = get_search_backend()

        parent_id = request.GET.get('parent_id', False)

        ocr_lang = request.user.preferences['ocr__OCR_Language']
        ocr_lang = ocr_lang.lower()

        if parent_id:
            descendent_ids = [
                str(desc.id)
                for desc in models.BaseTreeNode.objects.get_queryset_descendants(
                    models.BaseTreeNode.objects.filter(id=parent_id)
                )
            ]
        else:
            descendent_ids = []

        results = backend.search(search_term, models.Page)
        qs = models.BaseTreeNode.objects.filter(
            id__in=[p.document.basetreenode_ptr_id for p in results]
        )

        return qs

    def get_search_results(self, request, queryset, search_term):
        use_distinct = False

        # get either all documents qs or only documents from specified parent
        # i.e. all docs in specified folder - in case search is folder.
        qs = self.get_qs_from_raw_sql(request, search_term)

        qs_result = queryset

        if not search_term:
            return qs_result, use_distinct

        qs_result = qs

        return qs_result, use_distinct

    def formated_item_link(self, obj, length=17):

        is_folder = False
        truncator = Truncator(obj.title)
        if obj.polymorphic_ctype.name == 'Folder':
            is_folder = True

        if is_folder:
            css_class = 'folder'
            url = reverse(
                'admin:core_basetreenode_changelist_obj',
                args=(quote(obj.id),),
                current_app='boss'
            )
            link = format_html(
                '<a href="{}" class="{}" data-id="{}" alt="{}">{}</a>',
                url,
                css_class,
                obj.id,
                obj.title,
                truncator.chars(17, truncate='...')
            )
        else:
            css_class = 'document'
            # this thing queries S3 ,which performacewise kills whole app
            # plus adds $ to costs
            # ocr_status = obj.document.ocr_status
            url = reverse(
                'admin:core_basetreenode_change',
                args=(quote(obj.id),),
                current_app='boss'
            )
            link = format_html(
                '<a href="{}" data-id="{}" class="{} document_id" alt="{}">'
                '{}</a>',
                url,
                obj.id,
                css_class,
                obj.title,
                truncator.chars(17, truncate='...')
            )

        return link

    def title_with_class(self, obj):

        is_folder = False
        if obj.polymorphic_ctype.name in ('Folder', 'Ordner'):
            is_folder = True

        if is_folder:
            css_class = 'folder'
            url = reverse(
                'admin:core_basetreenode_changelist_obj',
                args=(quote(obj.id),),
                current_app='boss'
            )
            link = format_html(
                '<a href="{}" class="{}" data-id="{}" alt="{}">{}</a>',
                url,
                css_class,
                obj.id,
                obj.title,
                obj.title
            )
        else:
            css_class = 'document'
            # this thing queries S3 ,which performacewise kills whole app
            # plus adds $ to costs
            # ocr_status = obj.document.ocr_status
            url = reverse(
                'admin:core_basetreenode_change',
                args=(quote(obj.id),),
                current_app='boss'
            )
            link = format_html(
                '<a href="{}" data-id="{}" class="{} document_id" alt="{}">'
                '{}</a>',
                url,
                obj.id,
                css_class,
                obj.title,
                obj.title
            )

        return link

    title_with_class.short_description = 'Title'
    title_with_class.admin_order_field = 'title'

    def get_urls(self):
        from django.urls import path

        base_urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        extra_urls = [
            path(
                '<path:object_id>/list/',
                self.admin_site.admin_view(self.changelist_view_obj),
                name='%s_%s_changelist_obj' % info
            )
        ]

        return extra_urls + base_urls

    def get_changelist(self, request, **kwargs):
        return ChangeListBoss

    def get_queryset(self, request):
        """
        #### HACK 1 ####
        """
        qs = super().get_queryset(request)

        qs = qs.exclude(Q(title='Inbox'))

        within_parent_qs = None

        # Goes hand in hand with HACK 1 from changelist_view_obj function
        if getattr(request, 'object_id', False):
            node = models.BaseTreeNode.objects.get(id=request.object_id)
            within_parent_qs = qs.filter(parent=node)
        else:
            within_parent_qs = qs.filter(parent=None)

        # display only nodes which users has perm to read
        # (based on his or his groups permissions)
        allowed_ids = []
        for node in within_parent_qs:
            if request.user.has_perm(models.Access.PERM_READ, node):
                allowed_ids.append(node.id)

        return models.BaseTreeNode.objects.filter(id__in=allowed_ids)

    def changelist_view_obj(self, request, object_id):
        """
        #### HACK 1 ####
        """
        # Problem, for BaseTreeNodeAdmin wrapper, a new view
        # was added - changelist_view with object_id. This view
        # will display same thing as normal/admin standard changeview
        # except it will limit only to basenodetree objects of same level.
        # This enables browsing of objects simlar to file system fashion.
        # The problem is that changelist_view uses a queryset without "dynamic"
        # object - current request's object id. To filter queryset by current
        # object level, we pass object it to request object. This is a HACK
        # because it RELIES on THE FACT THAT INTERNALLY
        # super().changelist_view() USES SAME request object as argument to
        # self.get_queryset(...)
        # Maybe a good idea will be to replay this HACK
        # with some sort of middleware?

        request.object_id = object_id
        try:
            obj = models.BaseTreeNode.objects.get(id=object_id)
        except (models.BaseTreeNode.DoesNotExist):
            return None
        context = {}

        user_settings = request.user.preferences

        context['views__documents_view'] = user_settings.get(
            'views__documents_view',
            no_cache=True
        )

        context['object'] = obj
        return super().changelist_view(
            request,
            extra_context=context
        )

    def changelist_view(self, request, extra_context=None):
        additional_context = {}
        user_settings = request.user.preferences
        additional_context['views__documents_view'] = user_settings.get(
            'views__documents_view',
            no_cache=True,
        )
        # If no 'object' key is present in context, then when object is ref
        # in admin/polymorphic_tree/change_list.html, even with
        # {% if object %} {% end %} - django complains!
        additional_context['object'] = None
        if extra_context:
            extra_context.update(additional_context)
        else:
            extra_context = additional_context.copy()

        return super().changelist_view(
            request,
            extra_context=extra_context
        )

    def has_module_permission(self, request):
        return request.user.has_perm("vml_documents")

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('documents.delete', obj)

    def has_add_permission(self, request, obj=None):
        return request.user.has_perm("vml_documents")


class DynamicPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'setting_value',
        'setting_description',
    )

    def setting_description(self, obj):
        return obj.help_text

    setting_description.short_description = 'Description'

    def setting_value(self, obj):
        if obj.name == 'OCR_Language':
            return lang_human_name(obj.raw_value)

        return obj.raw_value

    setting_value.short_description = 'Value'

    fields = ('name', 'raw_value', )

    readonly_fields = ('name', )

    if preferences_settings.ADMIN_ENABLE_CHANGELIST_FORM:
        list_editable = ('raw_value',)

    list_filter = (('section', SectionFilter),)

    if preferences_settings.ADMIN_ENABLE_CHANGELIST_FORM:
        def get_changelist_form(self, request, **kwargs):
            return self.changelist_form

    def section_name(self, obj):
        try:
            return obj.registry.section_objects[obj.section].verbose_name
        except KeyError:
            pass
        return obj.section

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)

        # HACK
        # User preferences will be created when accessed first time
        # Without it this line, per instance models are not created
        request.user.preferences.all()
        # END of HACK
        qs = qs.filter(instance=request.user)

        return qs

    def has_module_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class GlobalPreferenceAdmin(DynamicPreferenceAdmin):
    form = UserSinglePreferenceForm
    changelist_form = UserPreferenceModel


class PerInstancePreferenceAdmin(DynamicPreferenceAdmin):
    list_display = DynamicPreferenceAdmin.list_display
    raw_id_fields = ('instance',)
    form = UserSinglePreferenceForm
    changelist_form = UserSinglePreferenceForm


class UserAdminEx(UserAdmin):

    change_password_form = forms.DgPasswordChangeForm

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff'
    )

    list_filter = ()

    fieldsets = (
        ('Main Info', {
            'fields': ('username', 'password'),
            'classes': ('vertical', )
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email'),
            'classes': ('vertical', )
        }),
        ('User & Permissions', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('vertical', )
        }),
    )


class GroupAdminEx(GroupAdmin):

    fieldsets = (
        ('Permissions', {
            'fields': ('name', 'permissions'),
            'classes': ('vertical', )
        }),
    )

    def has_module_permission(self, request):
        return request.user.has_perm('vml_root')

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('shorter_digest', 'created', 'expiry')
    fields = ('hours', )
    form = forms.AuthTokenForm
    raw_id_fields = ('user',)

    def shorter_digest(self, obj):
        return f"{obj.digest[:16]}..."

    shorter_digest.short_description = 'Digest'
    shorter_digest.admin_order_field = 'digest'

    def get_queryset(self, request):
        """ Manage only tokens current user"""
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """
        Create token using Knox API. Tokens are created only
        on Add action.
        """
        if not change:  # i.e. create new token only on "Add" action.
            new_object, token = AuthToken.objects.create(
                request.user,
                expiry=timedelta(hours=form.cleaned_data['hours'])
            )
            obj.user = request.user

            obj.token_key = new_object.token_key
            obj.digest = new_object.digest
            obj.expiry = new_object.expiry
            obj.salt = new_object.salt
            obj.created = new_object.created

            # Display (only once) unencrypted token
            message = format_html(_(
                "Remember the token: %(token)s. It won't be displayed again."
            ) % {'token': token})

            messages.add_message(
                request,
                messages.INFO,
                message,
            )

        super().save_model(request, obj, form, change)


bs_admin.site.register(UserPreferenceModel, PerInstancePreferenceAdmin)
bs_admin.site.register(models.BaseTreeNode, TreeNodeParentAdmin)
bs_admin.site.register(models.Document, DocumentNodeAdmin)
bs_admin.site.register(models.Folder, FolderNodeAdmin)
bs_admin.site.register(AuthToken, AuthTokenAdmin)
# also register admin wrappers of user and groups to bs_admin the
# same way admin app does automatically, just reuse admin code
bs_admin.site.register(User, UserAdminEx)
bs_admin.site.register(Group, GroupAdminEx)
