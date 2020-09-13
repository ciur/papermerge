from django.utils.translation import ugettext_lazy as _

from papermerge.contrib.admin.forms import TagForm
from papermerge.core.models import Tag
from papermerge.core.views import (
    AdminListView,
    AdminView,
    AdminChangeView
)


class TagsListView(AdminListView):
    model_class = Tag
    model_label = 'core.Tag'
    template_name = 'admin/tags.html'
    list_url = 'admin:tags'

    def get_queryset(self, request):
        return Tag.objects.filter(user=request.user)


class TagView(AdminView):
    title = _('New Tag')
    model_class = Tag
    form_class = TagForm
    template_name = 'admin/tag.html'
    action_url = 'admin:tag'
    list_url = 'admin:tags'


class TagChangeView(AdminChangeView):
    title = _('Edit Tag')
    model_class = Tag
    form_class = TagForm
    template_name = 'admin/tag.html'
    change_url = 'admin:tag_change'
    list_url = 'admin:tags'
