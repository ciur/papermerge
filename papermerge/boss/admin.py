from django.shortcuts import redirect

from django.contrib.admin import AdminSite
from django.urls import NoReverseMatch, reverse
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext_lazy
from django.utils.text import capfirst
from dynamic_preferences.registries import global_preferences_registry
from . import forms
from papermerge.core.models import Folder


class BossSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy('papermerge')

    # Text to put in each page's <h1>.
    site_header = gettext_lazy('papermerge')

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy('Dashboard')

    login_form = forms.BossAuthenticationForm

    # By default, django admin displays in admin index page
    # all registerd models grouped by app. Because of polymorphic
    # nature of BaseTreeNode (which might be Document or Folder)
    # we exclude the derived from BaseTreeNode models.
    # Please bear in mind, that because of business advantage,
    # user friendly name for BaseTreeNode model is "Documents" - do not
    # confuse it with real Document model which is just derived from
    # BaseTreeNode
    index_blacklisted_models = ['Document', 'Folder', 'UserPreferenceModel']

    def has_model_perm(self, request, model_admin):

        has_module_perms = model_admin.has_module_permission(request)

        if not has_module_perms:
            return False

        perms = model_admin.get_model_perms(request)
        # Check whether user has any perm for this module.
        # If so, add the module to the model_list.
        if True not in perms.values():
            return False

        return True

    def build_sidebar_item(self, request, model, model_admin):
        perms = model_admin.get_model_perms(request)
        app_label = model._meta.app_label
        info = (app_label, model._meta.model_name)

        model_dict = {
            'name': capfirst(model._meta.verbose_name_plural),
            'icon_name': model._meta.object_name.lower(),
            'perms': perms
        }
        if perms.get('change') or perms.get('view'):
            model_dict['view_only'] = not perms.get('change')
            try:
                model_dict['boss_url'] = reverse(
                    'boss:%s_%s_changelist' % info,
                    current_app=self.name
                )
            except NoReverseMatch:
                pass

        return model_dict

    def build_sidebar_inbox(self, request, model, model_admin):
        title = "Inbox"
        inbox, _ = Folder.objects.get_or_create(
            title=title,
            parent=None,
            user=request.user
        )
        children_count = inbox.get_descendants().count()
        model_dict = {
            'name': f"{title} ({children_count})",
            'icon_name': "inbox",
            'perms': {},
            'boss_url': reverse(
                'boss:core_basetreenode_changelist_obj', args=(inbox.id,)
            )
        }
        return model_dict

    def get_sidebar_items(self, request):
        models = {
            m._meta.object_name: [m, m_a]
            for m, m_a in self._registry.items()
        }
        result = []

        model, model_admin = models['BaseTreeNode']

        result.append(
            self.build_sidebar_item(request, model, model_admin)
        )

        result.append(
            self.build_sidebar_inbox(request, model, model_admin)
        )

        model, model_admin = models['Group']

        if self.has_model_perm(request, model_admin):
            result.append(
                self.build_sidebar_item(request, model, model_admin)
            )

        model, model_admin = models['User']

        if self.has_model_perm(request, model_admin):
            result.append(
                self.build_sidebar_item(request, model, model_admin)
            )

        return result

    def vml_get_app(self, app_list, app_name):
        for app in app_list:
            if app['app_label'] == app_name:
                return app

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        # at this point user might be anonymous
        return request.user.has_perm('vml_access')

    def filter_blacklisted_models(self, app_list):
        """
        Expects as input a list of app (hash with attributes), this
        is django specific. For details of structure of app_list object
        look at the return values of method self.get_app_list(request).
        Each app is examined for 'models' key, which is expected to be list
        as well. Every model in the list which has a object_name in
        self.index_blacklisted_models is filtered out.
        """
        for app in app_list:
            # exclude blacklisted models
            filtered_models = [
                mod for mod in app['models']
                if mod['object_name'] not in self.index_blacklisted_models
            ]
            app['models'] = filtered_models

        return app_list

    @never_cache
    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_list = self.get_app_list(request)

        pref_order_app_list = []
        pref_order_app_list.append(
            self.vml_get_app(app_list, 'core')
        )
        pref_order_app_list.append(
            self.vml_get_app(app_list, 'auth')
        )
        pref_order_app_list.append(
            self.vml_get_app(app_list, 'dynamic_preferences_users')
        )

        context = dict(
            self.each_context(request),
            title=self.index_title,
            app_list=pref_order_app_list,
        )
        context.update(extra_context or {})

        request.current_app = self.name

        # Sometime in future, we might revert return redirect to
        # return TemplateResponse(
        #    request, self.index_template or 'admin/index.html',
        #    context
        # )
        # basically this redirect makes Documents - main page inside boss.
        return redirect(
            'boss:core_basetreenode_changelist'
        )

    def each_context(self, request):
        context = super().each_context(request)

        app_list = self.get_app_list(request)

        if not request.user.is_authenticated:
            return context

        context['app_list'] = self.filter_blacklisted_models(app_list)
        context['sidebar_items'] = self.get_sidebar_items(request)

        for app in app_list:
            # exclude blacklisted models
            filtered_models = [
                mod for mod in app['models']
                if mod['object_name'] not in self.index_blacklisted_models
            ]
            app['models'] = filtered_models

        pref_order_app_list = []
        pref_order_app_list.append(
            self.vml_get_app(app_list, 'core')
        )
        pref_order_app_list.append(
            self.vml_get_app(app_list, 'dynamic_preferences_users')
        )
        pref_order_app_list.append(
            self.vml_get_app(app_list, 'auth')
        )

        context['app_list'] = pref_order_app_list

        request.current_app = self.name

        keyname = 'user_storage_max_size'
        system_settings = global_preferences_registry.manager()
        # storage size setting is expressed in MB,
        # but then we use in view django's filesizeformat template tag
        context[keyname] = system_settings[
            'system_settings__user_storage_size'
        ] * 1024  # adjust here because of filesizeformat template tag

        return context


site = BossSite(name="boss")
