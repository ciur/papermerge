from django.db import router
from django.db.models import Q
from django.contrib import messages
from django.contrib.admin import helpers
from django.utils.translation import gettext as _
from django.contrib.admin.utils import get_deleted_objects, model_ngettext
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse

from papermerge.core.models import BaseTreeNode
"""
Classes in this module are designed to overwrite respective classes in
django.contrib.admin.option. These classes are mixedin in class wished to
to be altered. Class need to be inserted such way to be before altered class
in MRO chain.
"""


class BaseModelBoss:
    """
    Mixin designed to overwrite methods from
    django.contrib.admin.options.BaseModelAdmin
    """

    def get_field_queryset(self, db, db_field, request):
        """
        If the ModelAdmin specifies ordering, the queryset should respect that
        ordering.  Otherwise don't specify the queryset, let the field decide
        (return None in that case).
        """
        qs = None
        related_admin = self.admin_site._registry.get(
            db_field.remote_field.model
        )
        if related_admin is not None:
            qs = db_field.remote_field.model._default_manager.using(db)
            ordering = related_admin.get_ordering(request)
            if ordering is not None and ordering != ():
                qs = qs.order_by(*ordering)

        return qs

    def save_model(self, request, obj, form, change):
        """
        Save model per current user.
        """
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Will show in dropdown box only folders/MPTT models of current user.
        """
        if db_field.name == "parent":
            kwargs["queryset"] = BaseTreeNode.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions is not None and 'delete_selected' in actions:
            actions['delete_selected'] = (
                self.delete_selected_boss,
                'delete_selected',
                _('Delete selected %(verbose_name_plural)s'))
        return actions

    def delete_selected_boss(self, modeladmin, request, queryset):
        """
        Default action which deletes the selected objects.

        This action first displays a confirmation page which shows all the
        deletable objects, or, if the user has no permission one of the related
        childs (foreignkeys), a "permission denied" message.

        Next, it deletes all selected objects and redirects back to the change
        list.
        """
        opts = modeladmin.model._meta
        app_label = opts.app_label
        # Check that the user has delete permission for the actual model
        for obj in queryset:
            if not modeladmin.has_delete_permission(request, obj):
                raise PermissionDenied

        using = router.db_for_write(modeladmin.model)
        # Populate deletable_objects, a data structure of all related objects
        # that will also be deleted.
        deletable_objects, model_count, x, y = get_deleted_objects(
            queryset, opts, request.user, modeladmin.admin_site, using)

        # The user has already confirmed the deletion.
        # Do the deletion and return None to display the change list
        # view again.
        if request.POST:
            n = queryset.count()
            if n:
                for obj in queryset:
                    obj_display = str(obj)
                    modeladmin.log_deletion(request, obj, obj_display)
                queryset.delete()
                modeladmin.message_user(
                    request, _("Successfully deleted %(count)d %(items)s.") % {
                        "count": n, "items": model_ngettext(modeladmin.opts, n)
                    }, messages.SUCCESS)
            # Return None to display the change list page again.
            return None

        objects_name = model_ngettext(queryset)

        title = _("Are you sure?")

        context = dict(
            modeladmin.admin_site.each_context(request),
            title=title,
            objects_name=str(objects_name),
            deletable_objects=[deletable_objects],
            model_count=dict(model_count).items(),
            queryset=queryset,
            perms_lacking=False,
            protected=False,
            opts=opts,
            action_checkbox_name=helpers.ACTION_CHECKBOX_NAME,
            media=modeladmin.media,
        )

        request.current_app = modeladmin.admin_site.name

        # Display the confirmation page
        return TemplateResponse(
            request, modeladmin.delete_selected_confirmation_template or [
                "admin/%s/%s/delete_selected_confirmation.html" % (
                    app_label, opts.model_name
                ),
                "admin/%s/delete_selected_confirmation.html" % app_label,
                "admin/delete_selected_confirmation.html"
            ], context)
