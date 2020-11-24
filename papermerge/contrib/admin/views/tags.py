from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError


from papermerge.contrib.admin.forms import TagForm
from papermerge.core.models import Tag
from papermerge.core.views import (
    PaginationMixin,
    DeleteEntriesMixin
)


class TagsView(LoginRequiredMixin):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('admin:tags')


class TagsListView(TagsView, PaginationMixin, DeleteEntriesMixin, ListView):

    title = _("Tags")

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(user=self.request.user)


class TagCreateView(TagsView, CreateView):
    title = _('New Tag')

    def form_valid(self, form):
        # set fields which user does not have access to
        form.instance.user = self.request.user

        try:
            form.instance.full_clean()
        except ValidationError:
            form._errors['name'] = [
                _('Tag name duplicate')
            ]
            del form.cleaned_data["name"]

            return super().form_invalid(form)

        return super().form_valid(form)


class TagUpdateView(TagsView, UpdateView):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit'
        context['action_url'] = reverse_lazy(
            'tag-update',
            args=(self.object.pk,)
        )
        return context
