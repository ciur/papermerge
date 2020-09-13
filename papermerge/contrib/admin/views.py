from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from papermerge.search.backends import get_search_backend
from papermerge.core.models import (
    Page,
    Folder,
    BaseTreeNode,
    Access,
    Tag
)
from papermerge.core.views import AdminListView, AdminView

from .models import LogEntry
from .forms import (
    LogEntryForm,
    TagForm
)


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


class LogsListView(AdminListView):
    model_class = LogEntry
    model_label = 'admin.LogEntry'
    template_name = 'admin/log_entries.html'

    def get_queryset(self, request):
        if request.user.is_superuser:
            # superuser sees all logs
            return LogEntry.objects.all()

        logs = LogEntry.objects.filter(user=request.user)

        return logs


class TagsListView(AdminListView):
    model_class = Tag
    model_label = 'core.Tag'
    template_name = 'admin/tags.html'

    def get_queryset(self, request):
        return Tag.objects.filter(user=request.user)


class LogFormView(AdminView):
    model = LogEntry
    form_class = LogEntryForm
    url = 'admin:log'
    template_name = 'admin/log_entry.html'
    title = _('Log Entry')


class TagFormView(AdminView):
    model = Tag
    form_class = TagForm
    url = 'admin:tag'
    template_name = 'admin/tag.html'
    title = _('Tag')


@login_required
def tag_change_view(request, id):
    tag = get_object_or_404(Tag, id=id)

    action_url = reverse('admin:tag_change', args=(id,))
    form = TagForm(
        request.POST or None,
        instance=tag
    )

    if form.is_valid():
        form.save()
        return redirect("admin:tags")

    return render(
        request,
        'admin/tag.html',
        {
            'form': form,
            'action_url': action_url,
            'title': _('Edit Tag')
        }
    )
