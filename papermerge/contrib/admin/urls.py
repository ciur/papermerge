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
        'logs', views.logs_view, name="logs"
    ),

    path(
        'log/<int:id>/', views.log_view, name="log"
    ),
    path(
        'tags', views.tags_view, name="tags"
    ),
    path(
        'tag/<int:id>/', views.tag_view, name="tag"
    ),
    path(
        'tag/<int:id>/change',
        views.tag_change_view, name='tag_change'
    ),
]
