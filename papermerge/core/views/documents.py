import os
import json
import logging

from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    Http404
)
from django import views
from django.contrib.auth.decorators import login_required

from pmworker.pdfinfo import get_pagecount
from mglib.step import Step
from mglib.shortcuts import extract_img

from papermerge.core.storage import default_storage
from papermerge.core.lib.hocr import Hocr

from papermerge.core.models import (
    Folder, Document, BaseTreeNode, Access
)
from papermerge.core.tasks import ocr_page

logger = logging.getLogger(__name__)


@login_required
def document(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        return render(request, "admin/document_404.html")

    if not request.is_ajax():
        return render(
            request,
            'admin/document.html',
            {
                'pages': doc.pages.all(),
                'document': doc
            }
        )
    # so, ajax only here
    if request.method == 'POST':
        # ajax + post
        pass

    # ajax + GET here
    return HttpResponse(
        json.dumps({'document': doc.to_dict()}),
        content_type="application/json",
    )


@login_required
@require_POST
def cut_node(request):
    data = json.loads(request.body)
    node_ids = [item['id'] for item in data]

    # request.clipboard.nodes = request.nodes
    request.nodes.add(node_ids)

    return HttpResponse(
        json.dumps({
            'msg': 'OK'
        }),
        content_type="application/json"
    )


@login_required
def clipboard(request):
    if request.method == 'GET':

        return HttpResponse(
            # request.nodes = request.clipboard.nodes
            json.dumps({'clipboard': request.nodes.all()}),
            content_type="application/json",
        )

    return HttpResponse(
        json.dumps({'clipboard': []}),
        content_type="application/json",
    )


@login_required
@require_POST
def paste_pages(request):
    """
    Paste pages in a changelist view.
    This means a new document instance
    is created.
    """
    data = json.loads(request.body)
    parent_id = data.get('parent_id', None)

    if parent_id:
        parent_id = int(parent_id)

    Document.paste_pages(
        user=request.user,
        parent_id=parent_id,
        doc_pages=request.pages.all()
    )

    request.pages.clear()

    return HttpResponse(
        json.dumps({'msg': 'OK'}),
        content_type="application/json",
    )


@login_required
@require_POST
def paste_node(request):
    data = json.loads(request.body)

    if not data:
        return HttpResponseBadRequest(
            json.dumps({
                'msg': 'Payload empty'
            }),
            content_type="application/json"
        )

    parent_id = data.get('parent_id', False)

    if parent_id:
        parent = BaseTreeNode.objects.filter(id=parent_id).first()
    else:
        parent = None

    # request.clipboard.nodes = request.nodes
    node_ids = request.nodes.all()

    # iterate through all node ids and change their
    # parent to new one (parent_id)
    for node in BaseTreeNode.objects.filter(id__in=node_ids):
        node.refresh_from_db()
        if parent:
            parent.refresh_from_db()
        Document.objects.move_node(node, parent)

    # request.clipboard.nodes = request.nodes
    request.nodes.clear()

    return HttpResponse(
        json.dumps({
            'msg': 'OK'
        }),
        content_type="application/json"
    )


@login_required
def rename_node(request, id):
    """
    Renames a node (changes its title field).
    """

    data = json.loads(request.body)
    title = data.get('title', None)

    if not title:
        return HttpResponse(
            json.dumps({'msg': 'Missing title'}),
            content_type="application/json",
        )

    node = get_object_or_404(BaseTreeNode, id=id)

    node.title = title
    node.save()

    return HttpResponse(
        json.dumps({'msg': "OK"}),
        content_type="application/json",
    )


@login_required
@require_POST
def create_folder(request):
    """
    Creates a new folder.

    Mandatory parameters parent_id and title:
    * If either parent_id or title are missing - does nothing.
    * If parent_id < 0 => creates a folder with parent root.
    * If parent_id >= 0 => creates a folder with given parent id.
    """
    data = json.loads(request.body)
    parent_id = data.get('parent_id', -1)
    title = data.get('title', False)

    if not (parent_id or title):
        logger.info(
            "Invalid params for create_folder: parent=%s title=%s",
            parent_id,
            title
        )
        return HttpResponseBadRequest(
            json.dumps({
                'msg': 'Both parent_id and title empty'
            }),
            content_type="application/json"
        )
    try:
        parent_id = int(parent_id)
    except ValueError:
        parent_id = -1

    if int(parent_id) < 0:
        parent_folder = None
    else:
        parent_folder = Folder.objects.filter(id=parent_id).first()
        # if not existing parent_id was given, redirect to root
        if not parent_folder:
            return HttpResponseBadRequest(
                json.dumps({
                    'msg': f"Parent with id={parent_id} does not exist"
                }),
                content_type="application/json"
            )

    folder = Folder.objects.create(
        title=title,
        parent=parent_folder,
        user=request.user
    )

    return HttpResponse(
        json.dumps(
            folder.to_dict()
        )
    )


class DocumentsUpload(views.View):
    def post(self, request):
        files = request.FILES.getlist('file')
        if not files:
            logger.warning(
                "POST request.FILES is empty. Forgot adding file?"
            )
            return HttpResponseBadRequest(
                "Missing input file"
            )

        if len(files) > 1:
            logger.warning(
                "More then one files per ajax? how come?"
            )
            return HttpResponse(
                json.dumps({}),
                content_type="application/json",
                status_code=400
            )

        f = files[0]

        logger.debug("upload for f=%s user=%s", f, request.user)

        user = request.user
        size = os.path.getsize(f.temporary_file_path())
        parent_id = request.POST.get('parent', "-1")
        if parent_id and "-1" in parent_id:
            parent_id = None

        lang = request.POST.get('language')
        notes = request.POST.get('notes')
        page_count = get_pagecount(f.temporary_file_path())
        logger.info("creating document {}".format(f.name))

        doc = Document.create_document(
            user=user,
            title=f.name,
            size=size,
            lang=lang,
            file_name=f.name,
            parent_id=parent_id,
            notes=notes,
            page_count=page_count
        )
        logger.debug(
            "uploading to {}".format(doc.path.url())
        )

        default_storage.copy_doc(
            src=f.temporary_file_path(),
            dst=doc.path.url()
        )

        for page_num in range(1, page_count + 1):
            ocr_page.apply_async(kwargs={
                'user_id': user.id,
                'document_id': doc.id,
                'file_name': f.name,
                'page_num': page_num,
                'lang': lang}
            )

        # upload only one file at time.
        # after each upload return a json object with
        # following fields:
        #
        # - title
        # - preview_url
        # - doc_id
        # - action_url  -> needed for renaming/deleting selected item
        #
        # with that info a new thumbnail will be created.

        # action_url = reverse(
        #     'boss:core_basetreenode_change', args=(doc.id,)
        # )

        preview_url = reverse(
            'core:preview', args=(doc.id, 200, 1)
        )

        result = {
            'title': doc.title,
            'doc_id': doc.id,
            'action_url': "",
            'preview_url': preview_url
        }
        logger.info("and response is!")
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


@login_required
def usersettings(request, option, value):

    if option == 'documents_view':
        user_settings = request.user.preferences
        if value in ('list', 'grid'):
            user_settings['views__documents_view'] = value
            user_settings['views__documents_view']

    return HttpResponseRedirect(
        request.META.get('HTTP_REFERER')
    )


@login_required
def hocr(request, id, step=None, page="1"):

    logger.debug(f"hocr for doc_id={id}, step={step}, page={page}")

    try:
        doc = Document.objects.get(id=id)
    except Document.DoesNotExist:
        raise Http404("Document does not exists")

    doc_path = doc.path

    if request.user.has_perm(Access.PERM_READ, doc):
        # document absolute path
        doc_abs_path = default_storage.abspath(doc_path.url())
        if not os.path.exists(
            doc_abs_path
        ):
            raise Http404("HOCR data not yet ready.")

        page_count = get_pagecount(doc_abs_path)
        if page > page_count or page < 0:
            raise Http404("Page does not exists")

        page_path = doc.page_paths[page]
        hocr_abs_path = default_storage.abspath(page_path.hocr_url())

        logger.debug(f"Extract words from {hocr_abs_path}")

        if not os.path.exists(hocr_abs_path):
            raise Http404("HOCR data not yet ready.")

        # At this point local HOCR data should be available.
        hocr = Hocr(
            hocr_file_path=hocr_abs_path
        )

        return HttpResponse(
            json.dumps({
                'hocr': hocr.good_json_words(),
                'hocr_meta': hocr.get_meta()
            }),
            content_type="application/json",
        )

    return HttpResponseForbidden()


@login_required
def preview(request, id, step=None, page="1"):

    try:
        doc = Document.objects.get(id=id)
    except Document.DoesNotExist:
        raise Http404("Document does not exists")

    if request.user.has_perm(Access.PERM_READ, doc):
        page_path = doc.get_page_path(
            page_num=page,
            step=Step(step),
        )
        img_abs_path = default_storage.abspath(
            page_path.img_url()
        )

        if not os.path.exists(img_abs_path):
            logger.debug(
                f"Preview image {img_abs_path} does not exists. Generating..."
            )
            extract_img(
                page_path, media_root=settings.MEDIA_ROOT
            )

        try:
            with open(img_abs_path, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        except IOError:
            raise

    return redirect('core:index')


@login_required
def document_download(request, id):

    try:
        doc = Document.objects.get(id=id)
    except Document.DoesNotExist:
        raise Http404("Document does not exists")

    if doc.user.username == request.user.username:
        try:
            file_handle = open(default_storage.abspath(
                doc.path.url()
            ), "rb")
        except OSError:
            logger.error(
                "Cannot open local version of %s" % doc.path.url()
            )
            # return redirect(
            #     'boss:core_basetreenode_changelist_obj', args=(id,)
            # )
            return redirect('browse')

        resp = HttpResponse(
            file_handle.read(),
            content_type="application/pdf"
        )
        disposition = "attachment; filename=%s" % doc.title
        resp['Content-Disposition'] = disposition
        file_handle.close()
        return resp

    # return redirect(
    #     'boss:core_basetreenode_changelist_obj', args=(id,)
    # )
    return redirect('browse')
