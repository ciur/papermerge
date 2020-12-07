from django.views.generic.base import ContextMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.contrib import messages


class RequiredPermissionMixin:

    def dispatch(self, request, *args, **kwargs):

        if not hasattr(self, 'required_permission'):
            return self.handle_no_permission()

        req_permission = getattr(self, 'required_permission')

        if not self.request.user.has_perm(req_permission):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class CommonListMixin(ContextMixin):
    """
    Provides common context for admin/object_list.html
    """

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['action_url'] = self.action_url
        context['success_url'] = self.success_url
        context['new_object_url'] = self.new_object_url
        context['title'] = self.title
        context['delete_selected_msg'] = self.get_delete_selected_msg()
        context['empty_list_msg'] = self.get_empty_list_msg()
        context['model_name_title'] = self.get_model_name_plu().capitalize()

        return context

    def get_model_name_plu(self):
        return self.model._meta.verbose_name_plural

    def get_delete_selected_msg(self):

        msg = _("Delete selected %(model_name_plu)s") % {
            'model_name_plu': self.get_model_name_plu()
        }

        return msg

    def get_empty_list_msg(self):

        msg = _("No %(model_name_plu)s so far") % {
            'model_name_plu': self.model._meta.verbose_name_plural
        }

        return msg


class DeleteEntriesMixin:
    """
    Handles HTTP POST with 'delete selected'.
    """

    def get_delete_entries(self, selection):
        return self.get_queryset().filter(
            id__in=selection
        )

    def post(self, request):
        """
        Delete selected entries
        """
        selected_action = request.POST.getlist('_selected_action')

        go_action = request.POST['action']
        if go_action == 'delete_selected':
            deleted, row_count = self.get_delete_entries(
                selection=selected_action
            ).delete()

            model_label = self.model._meta.label
            count = row_count.get(model_label, 0)
            msg = _(
                "%(count)s selected entries were deleted."
            ) % {
                'count': count
            }
            messages.info(self.request, msg)

        return redirect(self.success_url)


class PaginationMixin:

    PER_PAGE = 10

    def get_context_data(self, **kwargs):

        objs = self.get_queryset()
        page_number = int(self.request.GET.get('page', 1))

        paginator = Paginator(objs, per_page=self.PER_PAGE)
        num_pages = paginator.num_pages
        page_obj = paginator.get_page(page_number)

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

        context = super().get_context_data(**kwargs)
        context.update({
            'object_list': page_obj.object_list,
            'pages': pages,
            'num_pages': num_pages,
            'page_number': page_number,
            'page': page_obj,
            # by the way, add title to the context as well
            'title': self.title
        })

        return context

