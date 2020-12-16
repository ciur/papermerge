from django.urls import path
from papermerge.contrib.admin import views

app_name = 'admin'

urlpatterns = [
    path(
        '', views.BrowseView.as_view(), name="index"
    ),
    path(
        'inbox/', views.inbox_view, name="inbox"
    ),
    path(
        'browse', views.BrowseView.as_view(), name="browse"
    ),
    path(
        'search', views.search, name="search"
    ),
    path(
        'logs', views.LogsListView.as_view(), name="logs"
    ),

    path(
        'log/<int:pk>/',
        views.LogUpdateView.as_view(),
        name="log-update"
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
        'users/',
        views.UsersListView.as_view(),
        name='users'
    ),
    path(
        'user/add/',
        views.UserCreateView.as_view(),
        name='user-add'
    ),
    path(
        'user/<int:pk>/',
        views.UserUpdateView.as_view(),
        name='user-update'
    ),
    path(
        'user/<int:pk>/change-password',
        views.UserChangePasswordView.as_view(),
        name='user-change-password'
    ),
    path(
        'roles/',
        views.RolesListView.as_view(),
        name='roles'
    ),
    path(
        'role/add/',
        views.RoleCreateView.as_view(),
        name='role-add'
    ),
    path(
        'role/<int:pk>/',
        views.RoleUpdateView.as_view(),
        name='role-update'
    ),
    path(
        'tokens/',
        views.TokensListView.as_view(),
        name='tokens'
    ),
    path(
        'token/add/',
        views.TokenCreateView.as_view(),
        name='token-add'
    ),
    path(
        'token/<int:pk>/',
        views.TokenUpdateView.as_view(),
        name='token-update'
    ),
    path(
        'automates/',
        views.AutomatesListView.as_view(),
        name='automates'
    ),
    path(
        'automate/add/',
        views.AutomateCreateView.as_view(),
        name='automate-add'
    ),
    path(
        'automate/<int:pk>',
        views.AutomateUpdateView.as_view(),
        name='automate-update'
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
