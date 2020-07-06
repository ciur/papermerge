from django.contrib.auth.decorators import login_required
from django.urls import include, path
from papermerge.core.views import access as access_views
from papermerge.core.views import api as api_views
from papermerge.core.views import documents as doc_views
from papermerge.core.views import nodes as node_views
from papermerge.core.views import metadata as metadata_views
from papermerge.core.views import preferences as preferences_views
from papermerge.core.views import tokens as tokens_views

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
        '<int:id>/download/',
        doc_views.document_download,
        name="document_download"
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
    path('nodes/', node_views.nodes_view, name="nodes"),
    path(
        'access/<int:id>', access_views.access, name="access"
    ),
    path(
        'metadata/<model>/<int:id>', metadata_views.metadata, name="metadata"
    ),
    path(
        'usergroups', access_views.user_or_groups, name="user_or_groups"
    ),
    path(
        'upload/',
        login_required(doc_views.DocumentsUpload.as_view()),
        name="upload"
    ),
    path(
        'create-folder/',
        doc_views.create_folder,
        name='create_folder'
    ),
    path(
        'rename-node/<slug:redirect_to>/',
        doc_views.rename_node,
        name='rename_node'
    ),
    path(
        'delete-node/',
        doc_views.delete_node,
        name='delete_node'
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
        'preferences/',
        preferences_views.preferences_view,
        name='preferences'
    ),
    path(
        'tokens/',
        tokens_views.tokens_view,
        name='tokens'
    ),
    path(
        'token/',
        tokens_views.token_view,
        name='token'
    )
]
