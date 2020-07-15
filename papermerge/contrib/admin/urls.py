from django.urls import path
from papermerge.contrib.admin import views

urlpatterns = [
    path(
        '', views.browse, name="index"
    ),
    path(
        'inbox/', views.inbox_view, name="inbox"
    ),
    path(
        'browse', views.browse, name="browse"
    ),
    path(
        'search', views.search, name="search"
    ),
]
