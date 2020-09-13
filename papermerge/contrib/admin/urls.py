from django.urls import path
from papermerge.contrib.admin import views

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
        'logs', views.LogsListView.as_view(), name="logs"
    ),

    path(
        'log/<int:id>/change',
        views.LogChangeView.as_view(),
        name="log_change"
    ),
    path(
        'tags', views.TagsListView.as_view(), name="tags"
    ),
    path(
        'tag/',
        views.TagView.as_view(),
        name="tag"
    ),
    path(
        'tag/<int:id>/change',
        views.TagChangeView.as_view(), name='tag_change'
    ),
    path(
        'groups/',
        views.GroupsListView.as_view(),
        name='groups'
    ),
    path(
        'group/',
        views.GroupView.as_view(),
        name='group'
    ),
    path(
        'group/<int:id>/change',
        views.GroupChangeView.as_view(),
        name='group_change'
    ),
]
