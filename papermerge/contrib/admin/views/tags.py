from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError


from papermerge.contrib.admin.forms import TagForm
from papermerge.core.models import Tag
from papermerge.contrib.admin.views import mixins as mix


class TagsView(LoginRequiredMixin):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('admin:tags')


class TagsListView(
    TagsView,
    mix.PaginationMixin,
    mix.DeleteEntriesMixin,
    generic.ListView
):

    title = _("Tags")

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(user=self.request.user)


class TagCreateView(TagsView, generic.CreateView):

    title = _('New Tag')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('New')
        context['action_url'] = reverse_lazy('admin:tag-add')

        return context

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


class TagUpdateView(TagsView, generic.UpdateView):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit'
        context['action_url'] = reverse_lazy(
            'admin:tag-update',
            args=(self.object.pk,)
        )
        return context
