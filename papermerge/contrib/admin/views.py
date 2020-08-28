from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ngettext
from django.contrib import messages

from papermerge.search.backends import get_search_backend
from papermerge.core.models import (
    Page,
    Folder,
    BaseTreeNode,
    Access
)
from papermerge.contrib.admin.models import LogEntry


@login_required
def browse(request):
    return render(
        request,
        "admin/index.html"
    )


@login_required
def inbox_view(request):

    try:
        inbox = Folder.objects.get(
            title=Folder.INBOX_NAME,
            user=request.user
        )
        root_node_id = inbox.id

    except Folder.DoesNotExist:
        root_node_id = None

    return render(
        request,
        "admin/index.html",
        {
            'root_node_id': root_node_id
        }
    )


@login_required
def search(request):
    search_term = request.GET.get('q')
    backend = get_search_backend()

    results_folders = backend.search(search_term, Folder)
    results_docs = backend.search(search_term, Page)

    qs_docs = BaseTreeNode.objects.filter(
        id__in=[
            p.document.basetreenode_ptr_id for p in results_docs
        ]
    )

    qs_docs = [
        node for node in qs_docs.all()
        if request.user.has_perm(Access.PERM_READ, node)
    ]

    # filter out all documents for which current user
    # does not has read access

    return render(
        request,
        "admin/search.html",
        {
            'results_docs': qs_docs,
            'results_folders': results_folders.results(),
            'search_term': search_term
        }
    )


@login_required
def logs_view(request):

    if request.method == 'POST':
        selected_action = request.POST.getlist('_selected_action')
        go_action = request.POST['action']

        if go_action == 'delete_selected':
            deleted, row_count = LogEntry.objects.filter(
                id__in=selected_action
            ).delete()

            if deleted:
                count = row_count['papermerge.contrib.admin.LogEntry']
                msg_sg = "%(count)s log was successfully deleted."
                msg_pl = "%(count)s logs were successfully deleted."
                messages.info(
                    request,
                    ngettext(msg_sg, msg_pl, count) % {'count': count}
                )

    if request.user.is_superuser():
        # superuser sees all logs
        logs = LogEntry.objects.all()
    else:
        logs = LogEntry.objects.filter(user=request.user)

    return render(
        request,
        'admin/logs.html',
        {
            'logs': logs,
        }
    )
