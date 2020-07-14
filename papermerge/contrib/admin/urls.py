from django.urls import path
from papermerge.contrib.admin import views

urlpatterns = [
    path(
        '', views.browse, name="index"
    ),
    path(
        'browse', views.browse, name="browse"
    ),
    path(
        'search', views.search, name="search"
    ),
]
