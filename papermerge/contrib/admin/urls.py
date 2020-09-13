from django.urls import path
from papermerge.contrib.admin import views
from papermerge.contrib.admin.views import (
    LogChangeView,
    LogsListView,
    TagView,
    TagsListView,
    TagChangeView,
)

app_name = 'admin'

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
    path(
        'logs', LogsListView.as_view(), name="logs"
    ),

    path(
        'log/<int:id>/change',
        LogChangeView.as_view(),
        name="log_change"
    ),
    path(
        'tags', TagsListView.as_view(), name="tags"
    ),
    path(
        'tag/',
        TagView.as_view(),
        name="tag"
    ),
    path(
        'tag/<int:id>/change',
        TagChangeView.as_view(), name='tag_change'
    ),
]
