import os
import json
import logging

from django.shortcuts import redirect
from django.urls import reverse
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


def index(request):
    return redirect('boss:core_basetreenode_changelist')


@login_required
def cut_node(request):
    if request.method == 'GET':
        return redirect('boss:core_basetreenode_changelist')

    node_ids = request.POST.getlist('node_ids[]', False)
    parent_id = request.POST.get('parent_id', False)

    # request.clipboard.nodes = request.nodes
    request.nodes.add(node_ids)

    if parent_id:
        return redirect(
            reverse(
                'boss:core_basetreenode_changelist_obj', args=(parent_id,)
            )
        )

    return redirect('boss:core_basetreenode_changelist')


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
def paste_pages(request):
    """
    Paste pages in a changelist view.
    This means a new document instance
    is created.
    """
    if request.method == 'GET':
        return redirect('boss:core_basetreenode_changelist')

    parent_id = request.POST.get('parent_id', False)

    Document.paste_pages(
        user=request.user,
        parent_id=parent_id,
        doc_pages=request.pages.all()
    )

    request.pages.clear()

    if parent_id:
        return redirect(
            reverse(
                'boss:core_basetreenode_changelist_obj', args=(parent_id,)
            )
        )

    return redirect('boss:core_basetreenode_changelist')


@login_required
def paste_node(request):
    if request.method == 'GET':
        return redirect('boss:core_basetreenode_changelist')

    parent_id = request.POST.get('parent_id', False)

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

    if parent_id:
        return redirect(
            reverse(
                'boss:core_basetreenode_changelist_obj', args=(parent_id,)
            )
        )

    return redirect('boss:core_basetreenode_changelist')


@login_required
def delete_node(request):
    """
    Delete selected nodes.

    Mandatory parameters node_ids[] and title:
    """
    if request.method == 'GET':
        return redirect('boss:core_basetreenode_changelist')

    node_ids = request.POST.getlist('node_ids[]', False)
    parent_id = request.POST.get('parent_id', False)

    BaseTreeNode.objects.filter(id__in=node_ids).delete()

    if parent_id:
        return redirect(
            reverse(
                'boss:core_basetreenode_changelist_obj', args=(parent_id,)
            )
        )
    else:
        return redirect('boss:core_basetreenode_changelist')


@login_required
def rename_node(request, redirect_to):
    """
    Renames a node (changes its title field).

    Mandatory parameters node_id and title.

    redirect_to = (change | list)
        change = will redirect to changeform of given doc
        list = will redirect to list view of given parent_id
    """
    if request.method == 'GET':
        return redirect('boss:core_basetreenode_changelist')

    node_id = request.POST.get('node_id', False)
    title = request.POST.get('title', False)

    if not (node_id and title):
        logger.info(
            "Invalid params for rename_node: node_id=%s title=%s",
            node_id,
            title
        )
        return redirect('boss:core_basetreenode_changelist')

    node = BaseTreeNode.objects.get(id=node_id)
    if not node:
        return redirect('boss:core_basetreenode_changelist')

    node.title = title
    node.save()

    # Node can be renamed in two places:
    # 1. In changeform view
    # 2. In changelist view
    # In case 1. redirect_to == 'change' in other case
    # redirect_to == 'list'
    if redirect_to == 'change':
        return redirect(
            reverse(
                'boss:core_basetreenode_change', args=(node_id,)
            )
        )
    # means redirect_to == 'list' i.e this rename was
    # called from changelist view.
    if node.parent_id:
        return redirect(
            reverse(
                'boss:core_basetreenode_changelist_obj', args=(node.parent_id,)
            )
        )
    else:
        return redirect('boss:core_basetreenode_changelist')


@login_required
def create_folder(request):
    """
    Creates a new folder.

    Mandatory parameters parent_id and title:
    * If either parent_id or title are missing - does nothing,
    just redirects to root folder.
    * If parent_id < 0 => creates a folder with parent root.
    * If parent_id >= 0 => creates a folder with given parent id.
    """
    if request.method == 'GET':
        return redirect('boss:core_basetreenode_changelist')

    parent_id = request.POST.get('parent_id', False)
    title = request.POST.get('title', False)

    if not (parent_id and title):
        logger.info(
            "Invalid params for create_folder: parent=%s title=%s",
            parent_id,
            title
        )
        return redirect('boss:core_basetreenode_changelist')

    if int(parent_id) < 0:
        parent_folder = None
    else:
        parent_folder = Folder.objects.filter(id=parent_id).first()
        # if not existing parent_id was given, redirect to root
        if not parent_folder:
            return redirect('boss:core_basetreenode_changelist')

    Folder.objects.create(
        title=title,
        parent=parent_folder,
        user=request.user
    )

    # must redirect to parent of created folder
    if int(parent_id) == -1:
        return redirect('boss:core_basetreenode_changelist')

    return redirect(
        reverse(
            'boss:core_basetreenode_changelist_obj', args=(parent_id,)
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

        action_url = reverse(
            'boss:core_basetreenode_change', args=(doc.id,)
        )

        preview_url = reverse(
            'core:preview', args=(doc.id, 200, 1)
        )

        result = {
            'title': doc.title,
            'doc_id': doc.id,
            'action_url': action_url,
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
            return redirect(
                'boss:core_basetreenode_changelist_obj', args=(id,)
            )

        resp = HttpResponse(
            file_handle.read(),
            content_type="application/pdf"
        )
        disposition = "attachment; filename=%s" % doc.title
        resp['Content-Disposition'] = disposition
        file_handle.close()
        return resp

    return redirect(
        'boss:core_basetreenode_changelist_obj', args=(id,)
    )
