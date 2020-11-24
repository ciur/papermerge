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
        'tags/', views.TagsListView.as_view(), name="tags"
    ),
    path(
        'tag/add/',
        views.TagCreateView.as_view(),
        name="tag-add"
    ),
    path(
        'tag/<int:pk>/',
        views.TagUpdateView.as_view(),
        name='tag-update'
    ),
    path(
        'groups/',
        views.GroupsListView.as_view(),
        name='groups'
    ),
    path(
        'group/add/',
        views.GroupCreateView.as_view(),
        name='group-add'
    ),
    path(
        'group/<int:pk>/',
        views.GroupUpdateView.as_view(),
        name='group-update'
    ),
    path(
        'automates/',
        views.AutomatesListView.as_view(),
        name='automates'
    ),
    path(
        'automate/',
        views.AutomateView.as_view(),
        name='automate'
    ),
    path(
        'automate/<int:id>/change',
        views.AutomateChangeView.as_view(),
        name='automate_change'
    ),
    path(
        'preferences/',
        views.preferences_view,
        name='preferences'
    ),
    path(
        'preferences/<str:section>/',
        views.preferences_section_view,
        name='preferences_section'
    ),
]
