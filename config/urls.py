from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog

from django.conf.urls import include

from django.conf import settings

js_info_dict = {
    'domain': 'django',
    'packages': None,
}


urlpatterns = [
    path('api/', include('papermerge.core.urls')),
]

for extra_urls in settings.EXTRA_URLCONF:
    urlpatterns.append(
        path('', include(extra_urls)),
    )
