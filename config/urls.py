from django.urls import path
from django.views.generic.base import RedirectView
from django.views.i18n import JavaScriptCatalog

from django.conf.urls import (
    include,
    handler400,
    handler403,
    handler404,
    handler500
)

from papermerge.boss.admin import site as boss_site
from django.conf.urls.static import static
from django.conf import settings

from allauth.account import views as allauth_views
from customers import views as customers_views

urlpatterns = [
    path('login/', boss_site.login, name="login"),
    # will redirect login from public login, to
    # a given tenant login url
    path(
        'redirect-login/',
        customers_views.redirect_login,
        name="redirect-login"
    ),
    path('register/', customers_views.signup, name="register"),
    # will redirect registration url a tenant, to
    # a public registration url
    path(
        'redirect-register/',
        customers_views.redirect_register,
        name="redirect-register"
    ),
    path(
        'register/thanks/',
        customers_views.RegistrationThanksView.as_view(),
        name="register_thanks"),
    path(
        'register/status/',
        customers_views.RegistrationStatusView.as_view(),
        name="register_status"),
    path(
        'register/company/check/',
        customers_views.company_check,
        name="company_check"
    ),
    path(
        'register/email/check/',
        customers_views.email_check,
        name="email_check"
    ),
    path(
        'reset/',
        allauth_views.password_reset,
        # ! name is important
        name="password_reset"
    ),
    # will redirect password reset from public tenant, to
    # a given tenant
    path(
        'redirect-reset/',
        customers_views.redirect_reset,
        name="redirect-reset"
    ),
    path(
        'forgot-company-name/',
        customers_views.forgot_company_name,
        name="forgot-company-name"
    ),
    path('admin/', boss_site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('papermerge.core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'papermerge.core.views.errors.bad_request_400_custom'
handler403 = 'papermerge.core.views.errors.permission_denied_403_custom'
handler404 = 'papermerge.core.views.errors.page_not_found_404_custom'
handler500 = 'papermerge.core.views.errors.server_error_500_custom'
