from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.views.i18n import JavaScriptCatalog

from django.conf.urls import include

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from allauth.account import views

from papermerge.contrib.admin.views import BrowseView


js_info_dict = {
    'domain': 'django',
    'packages': None,
}


favicon_view = RedirectView.as_view(
    url='/static/admin/img/favicon.ico',
    permanent=True
)

urlpatterns = [
    re_path(r'favicon\.ico$', favicon_view),
    path(
        'accounts/signup/',
        TemplateView.as_view(template_name="account/signup_disabled.html"),
        name="account_signup"
    ),
    # all paths from allauth.account (prefixes with accounts/) except signup
    path("accounts/login/", views.login, name="account_login"),
    path("accounts/logout/", views.logout, name="account_logout"),
    path(
        "accounts/password/change/",
        views.password_change,
        name="account_change_password",
    ),
    path(
        "accounts/password/set/",
        views.password_set,
        name="account_set_password"
    ),
    path(
        "accounts/inactive/",
        views.account_inactive,
        name="account_inactive"
    ),
    # E-mail
    path("accounts/email/", views.email, name="account_email"),
    path(
        "accounts/confirm-email/",
        views.email_verification_sent,
        name="account_email_verification_sent",
    ),
    re_path(
        r"^accounts/confirm-email/(?P<key>[-:\w]+)/$",
        views.confirm_email,
        name="account_confirm_email",
    ),
    # password reset
    path(
        "accounts/password/reset/",
        views.password_reset,
        name="account_reset_password"
    ),
    path(
        "accounts/password/reset/done/",
        views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "accounts/password/reset/key/done/",
        views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),
    path(
        'jsi18n/',
        JavaScriptCatalog.as_view(),
        js_info_dict,
        name='javascript-catalog'
    ),
    path('admin/', include('papermerge.contrib.admin.urls')),
    path('', include('papermerge.core.urls')),
    path('', BrowseView.as_view(), name='index'),
]

for extra_urls in settings.EXTRA_URLCONF:
    urlpatterns.append(
        path('', include(extra_urls)),
    )

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
