from django.urls import include, path
from .views import access as access_views
from .views import tags as tags_views
from .views import api as api_views
from .views import documents as doc_views
from .views import nodes as node_views
from .views import metadata as metadata_views
from .views import users as users_views
from .views import automates as automate_views

document_patterns = [
    path(
        '<int:doc_id>/',
        doc_views.document,
        name="document"
    ),
    path(
        '<int:id>/preview/page/<int:page>',
        doc_views.preview,
        name="preview"
    ),
    path(
        '<int:id>/preview/<int:step>/page/<int:page>',
        doc_views.preview,
        name="preview"
    ),
    path(
        '<int:id>/hocr/<int:step>/page/<int:page>',
        doc_views.hocr,
        name="hocr"
    ),
    path(
        'usersettings/<str:option>/<str:value>',
        doc_views.usersettings,
        name="usersettings"
    ),
]

app_name = 'core'

urlpatterns = [
    path(
        'document/', include(document_patterns)
    ),
    path('browse/', node_views.browse_view, name="browse"),
    path('browse/<int:parent_id>/', node_views.browse_view, name="browse"),
    path('breadcrumb/', node_views.breadcrumb_view, name="breadcrumb"),
    path(
        'breadcrumb/<int:parent_id>/',
        node_views.breadcrumb_view,
        name="breadcrumb"
    ),
    path('node/<int:node_id>', node_views.node_view, name="node"),
    # Node can be a document or a folder
    # Downloading entire folder by selecting it - makes perfect sense
    path(
        'node/<int:id>/download/',
        node_views.node_download,
        name="node_download"
    ),
    path(
        'node/by/title/<str:title>', node_views.node_by_title_view,
        name="node_by_title"
    ),
    path('nodes/', node_views.nodes_view, name="nodes"),
    # when user selected multiple documents and folders for download
    path('nodes/download/', node_views.nodes_download, name="nodes_download"),
    path(
        'node/<int:id>/access', access_views.access_view, name="access"
    ),
    path(
        'node/<int:node_id>/tags/', tags_views.tags_view, name="tags"
    ),
    path(
        'nodes/tags/', tags_views.nodes_tags_view, name="nodes_tags"
    ),
    path(
        'alltags/', tags_views.alltags_view, name="alltags"
    ),
    path(
        'metadata/<model>/<int:id>', metadata_views.metadata, name="metadata"
    ),
    path(
        'usergroups', access_views.user_or_groups, name="user_or_groups"
    ),
    path(
        'upload/',
        doc_views.upload,
        name="upload"
    ),
    path(
        'create-folder/',
        doc_views.create_folder,
        name='create_folder'
    ),
    path(
        'rename-node/<int:id>',
        doc_views.rename_node,
        name='rename_node'
    ),
    path(
        'cut-node/',
        doc_views.cut_node,
        name='cut_node'
    ),
    path(
        'paste-node/',
        doc_views.paste_node,
        name='paste_node'
    ),
    path(
        'paste-pages/',
        doc_views.paste_pages,
        name='paste_pages'
    ),
    path(
        'clipboard/',
        doc_views.clipboard,
        name='clipboard'
    ),
    path(
        'api/documents',
        api_views.DocumentsView.as_view(),
        name='api_documents'
    ),
    path(
        'api/document/upload/<str:filename>',
        api_views.DocumentUploadView.as_view(),
        name='api_document_upload'
    ),
    path(
        'api/document/<int:pk>/',
        api_views.DocumentView.as_view(),
        name='api_document'
    ),
    path(
        'api/document/<int:doc_id>/pages',
        api_views.PagesView.as_view(),
        name='api_pages'
    ),
    path(
        'api/document/<int:doc_id>/pages/cut',
        api_views.PagesCutView.as_view(),
        name='api_pages_cut'
    ),
    path(
        'api/document/<int:doc_id>/pages/paste',
        api_views.PagesPasteView.as_view(),
        name='api_pages_paste'
    ),
    path(
        'user/<int:id>/change-password',
        users_views.user_change_password_view, name='user_change_password'
    ),
    path(
        'automate/',
        automate_views.automate_view,
        name="automate_view"
    ),
    path(
        'automate/<int:automate_id>/',
        automate_views.automate_change_view, name="automate_change_view"
    ),
]
