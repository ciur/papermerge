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

urlpatterns = [
    path('login/', boss_site.login, name="login"),
    # will redirect login from public login, to
    # a given tenant login url
    path('admin/', boss_site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('papermerge.core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'papermerge.core.views.errors.bad_request_400_custom'
handler403 = 'papermerge.core.views.errors.permission_denied_403_custom'
handler404 = 'papermerge.core.views.errors.page_not_found_404_custom'
handler500 = 'papermerge.core.views.errors.server_error_500_custom'
