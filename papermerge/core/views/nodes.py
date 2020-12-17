import json
import logging

from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    Http404,
    HttpResponse
)
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import (
    get_object_or_404,
    redirect
)
from django.utils.translation import gettext as _
from django.core.files.temp import NamedTemporaryFile
from django.core.paginator import Paginator

from papermerge.core.models import (
    BaseTreeNode,
    Access,
    Folder,
    Automate,
    Tag
)
from papermerge.core import signal_definitions as signals
from papermerge.core.backup_restore import build_tar_archive
from papermerge.core.storage import default_storage

from .decorators import json_response
from .utils import sanitize_kvstore_list

logger = logging.getLogger(__name__)


PER_PAGE = 30


@json_response
@login_required
def browse_view(request, parent_id=None):
    nodes = BaseTreeNode.objects.filter(parent_id=parent_id).exclude(
        title=Folder.INBOX_NAME
    )
    tag = request.GET.get('tag', None)

    if tag:
        nodes = BaseTreeNode.objects.filter(tags__name__in=[tag]).exclude(
            title=Folder.INBOX_NAME
        )

    nodes_list = []
    parent_kv = []

    if parent_id:

        parent_node = get_object_or_404(
            BaseTreeNode, id=parent_id
        )

        for item in parent_node.kv.all():
            parent_kv.append(item.to_dict())

    # Will returns a dictionary. Each key of the dictionary
    # is the id of the node. Value of the key is permissions
    # dictionary e.g.
    # {
    #   '23': {"read": True, "delete": False },
    #   '24': {"read": True, "delete": False },
    #   '25': {"read": False, "delete": False }
    # }
    nodes_perms = request.user.get_perms_dict(
        nodes, Access.ALL_PERMS
    )
    readable_nodes = []
    for node in nodes:
        if nodes_perms[node.id].get(Access.PERM_READ, False):
            readable_nodes.append(node)

    page_number = request.GET.get('page', 1)
    if not page_number:
        page_number = 1

    page_number = int(page_number)

    paginator = Paginator(readable_nodes, per_page=PER_PAGE)
    num_pages = paginator.num_pages
    page_obj = paginator.get_page(page_number)

    for node in page_obj.object_list:
        node_dict = node.to_dict()
        # and send user_perms to the frontend client

        node_dict['user_perms'] = nodes_perms[node.id]

        if node.is_document():
            node_dict['img_src'] = reverse(
                'core:preview',
                args=(node.id, 4, 1)
            )
            node_dict['document_url'] = reverse(
                'core:document',
                args=(node.id,)
            )

        nodes_list.append(node_dict)

    # 1.   Number of pages < 7: show all pages;
    # 2.   Current page <= 4: show first 7 pages;
    # 3.   Current page > 4 and < (number of pages - 4): show current page,
    #       3 before and 3 after;
    # 4.   Current page >= (number of pages - 4): show the last 7 pages.

    if num_pages <= 7 or page_number <= 4:  # case 1 and 2
        pages = [x for x in range(1, min(num_pages + 1, 7))]
    elif page_number > num_pages - 4:  # case 4
        pages = [x for x in range(num_pages - 6, num_pages + 1)]
    else:  # case 3
        pages = [x for x in range(page_number - 3, page_number + 4)]

    if page_obj.has_previous():
        previous_page_number = page_obj.previous_page_number()
    else:
        previous_page_number = -1

    if page_obj.has_next():
        next_page_number = page_obj.next_page_number()
    else:
        next_page_number = -1

    return {
        'nodes': nodes_list,
        'parent_id': parent_id,
        'parent_kv': parent_kv,
        'pagination': {
            'page_number': page_number,
            'pages': pages,
            'num_pages': num_pages,
            'page': {
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': previous_page_number,
                'next_page_number': next_page_number,
            }
        }
    }


@json_response
@login_required
def breadcrumb_view(request, parent_id=None):

    nodes = []

    node = None
    try:
        node = BaseTreeNode.objects.get(id=parent_id)
    except BaseTreeNode.DoesNotExist:
        pass

    if node:
        nodes = [
            item.to_dict() for item in node.get_ancestors(include_self=True)
        ]

    return {
        'nodes': nodes,
    }


@json_response
@login_required
def node_by_title_view(request, title):
    """
    Useful in case of special folders like inbox (and trash in future).
    Returns node id, children_count, title of specified node's title.
    Title specified is insensitive (i.e. INBOX = Inbox = inbox).
    """
    node = get_object_or_404(
        BaseTreeNode,
        title__iexact=title
    )

    return {
        'id': node.id,
        'title': node.title,
        'children_count': node.get_children().count(),
        'url': reverse('node_by_title', args=('inbox',))
    }


@json_response
@login_required
def node_view(request, node_id):
    """
    GET or DELETE /node/<node_id>
    """
    try:
        node = BaseTreeNode.objects.get(id=node_id)
    except BaseTreeNode.DoesNotExist:
        ret = {
            'node': node.to_dict()
        }
        return ret, HttpResponseBadRequest.status_code

    if request.method == "DELETE":
        if request.user.has_perm(Access.PERM_DELETE, node):
            node.delete()
        else:
            msg = f"{request.user.username} does not have" +\
                f" permission to delete {node.title}"

            return msg, HttpResponseForbidden.status_code

        return 'OK'

    if request.method in ("PUT", "POST"):
        if not request.user.has_perm(Access.PERM_WRITE, node):
            return "Permission denied", HttpResponseForbidden.status_code

        node_data = json.loads(request.body)
        if 'kvstore' in node_data:
            metadata = node_data['kvstore']
            if isinstance(metadata, list):
                node.kv.update(
                    sanitize_kvstore_list(metadata)
                )

    if not request.user.has_perm(Access.PERM_READ, node):
        return "Permission denied", HttpResponseForbidden.status_code

    node_dict = node.to_dict()
    # minor hack to enable autocomplete for tag editor
    # in document view
    node_dict['alltags'] = [
        tag.to_dict()
        for tag in Tag.objects.filter(user=request.user)
    ]

    return {
        'node': node_dict
    }


@json_response
@login_required
def nodes_view(request):
    """
    GET or POST /nodes/
    """

    if request.method == "POST":

        data = json.loads(request.body)
        node_ids = [item['id'] for item in data]
        queryset = BaseTreeNode.objects.filter(id__in=node_ids)

        automates = Automate.objects.filter(
            dst_folder__in=queryset
        )
        if automates.count():
            msg = _(
                "Following Automates have references to folders "
                "you are trying to delete: "
            )
            msg += ", ".join([auto.name for auto in automates])
            msg += _(
                ". Please delete mentioned Automates frist."
            )

            return msg, HttpResponseBadRequest.status_code

        nodes_perms = request.user.get_perms_dict(
            queryset, Access.ALL_PERMS
        )
        node_titles = []
        for node in queryset:
            node_titles.append(
                node.title
            )
            if not nodes_perms[node.id].get(Access.PERM_DELETE, False):
                # if user does not have delete permission on
                # one node - forbid entire operation!
                msg = f"{request.user.username} does not have" +\
                    f" permission to delete {node.title}"

                return msg, HttpResponseForbidden.status_code
        # yes, user is allowed to delete all nodes,
        # proceed with delete opration
        queryset.delete()
        signals.nodes_deleted.send(
            sender='core.views.nodes.nodes_view',
            user_id=request.user.id,
            level=logging.INFO,
            message=_("Nodes deleted"),
            node_titles=node_titles,
            node_ids=node_ids
        )

        return 'OK'

    return 'OK'


@login_required
def node_download(request, id):
    """
    Any user with read permission on the node must be
    able to download it.

    Node is either documennt or a folder.
    """
    version = request.GET.get('version', None)

    try:
        node = BaseTreeNode.objects.get(id=id)
    except BaseTreeNode.DoesNotExist:
        raise Http404("Node does not exists")

    if request.user.has_perm(Access.PERM_READ, node):

        if node.is_document():
            try:
                file_handle = open(default_storage.abspath(
                    node.path().url(version=version)
                ), "rb")
            except OSError:
                logger.error(
                    "Cannot open local version of %s" % node.path.url()
                )
                return redirect('admin:browse')

            resp = HttpResponse(
                file_handle.read(),
                content_type="application/pdf"
            )
            disposition = "attachment; filename=%s" % node.title
            resp['Content-Disposition'] = disposition
            file_handle.close()

            return resp
        else:  # node is a folder

            with NamedTemporaryFile(prefix="download_") as fileobj:
                # collected into an archive all direct children of
                # selected folder
                node_ids = [_node.id for _node in node.get_children()]
                build_tar_archive(
                    fileobj=fileobj,
                    node_ids=node_ids
                )
                # reset fileobj to initial position
                fileobj.seek(0)
                data = fileobj.read()
                resp = HttpResponse(
                    data,
                    content_type="application/x-tar"
                )
                disposition = f"attachment; filename={node.title}.tar"
                resp['Content-Disposition'] = disposition

                return resp

    return HttpResponseForbidden()


@login_required
def nodes_download(request):
    """
    Download multiple nodes (documents and folders) packed
    as tar.gz archive.
    """

    node_ids = request.GET.getlist('node_ids[]')
    nodes = BaseTreeNode.objects.filter(
        id__in=node_ids
    )
    nodes_perms = request.user.get_perms_dict(
        nodes, Access.ALL_PERMS
    )
    for node in nodes:
        if not nodes_perms[node.id].get(
            Access.PERM_READ, False
        ):
            msg = _(
                "%s does not have permission to read %s"
            ) % (request.user.username, node.title)

            return msg, HttpResponseForbidden.status_code

    with NamedTemporaryFile(prefix="download_") as fileobj:
        build_tar_archive(
            fileobj=fileobj,
            node_ids=node_ids
        )
        # reset fileobj to initial position
        fileobj.seek(0)
        data = fileobj.read()
        resp = HttpResponse(
            data,
            content_type="application/x-tar"
        )
        disposition = "attachment; filename=download.tar"
        resp['Content-Disposition'] = disposition

        return resp
