from django.urls import path, include
from django.contrib.auth.decorators import login_required

from papermerge.core.views import documents as doc_views
from papermerge.core.views import access as access_views
from papermerge.core.views import api as api_views


document_patterns = [
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
    path('', doc_views.index, name="index"),
    path(
        'document/', include(document_patterns)
    ),
    path(
        'access/<int:id>', access_views.access, name="access"
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
        'clipboard/',
        doc_views.clipboard,
        name='clipboard'
    ),
    path(
        'api/documents',
        api_views.documents,
        name='api_documents'
    ),
    path(
        'api/document/<int:pk>/',
        api_views.document,
        name='api_document'
    )
]
