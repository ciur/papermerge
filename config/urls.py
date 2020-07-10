from django.urls import path, re_path
from django.views.generic.base import RedirectView

from django.conf.urls import include

from django.conf.urls.static import static
from django.conf import settings

favicon_view = RedirectView.as_view(
    url='/static/admin/img/favicon.ico',
    permanent=True
)

urlpatterns = [
    re_path(r'favicon\.ico$', favicon_view),
    path('accounts/', include('allauth.urls')),
    path('', include('papermerge.contrib.admin.urls')),
    path('', include('papermerge.core.urls')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
