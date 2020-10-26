from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.views.i18n import JavaScriptCatalog

from django.conf.urls import include

from django.conf.urls.static import static
from django.conf import settings

from papermerge.contrib.admin.views import browse as index_view


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
    path('accounts/', include('allauth.urls')),
    path(
        'jsi18n/',
        JavaScriptCatalog.as_view(),
        js_info_dict,
        name='javascript-catalog'
    ),
    path('admin/', include('papermerge.contrib.admin.urls')),
    path('', include('papermerge.core.urls')),
    path('', index_view, name='index'),
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
