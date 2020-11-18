from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.utils.translation import ngettext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View


class CommonView(View):
    def is_allowed(self, request):
        if hasattr(self, 'only_superuser'):
            if getattr(self, 'only_superuser'):
                return request.user.is_superuser

        return True


@method_decorator(login_required, name='dispatch')
class AdminChangeView(CommonView):
    """
    View/Update exising entries
    """

    def get(self, request, id, **kwargs):
        if not self.is_allowed(request):
            return HttpResponseForbidden()

        entry = get_object_or_404(
            self.model_class, id=id
        )
        form = self.form_class(
            instance=entry
        )
        change_url = reverse(
            self.change_url, args=(id,)
        )

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'action_url': change_url,
                'title': self.title
            }
        )

    def post(self, request, id, **kwargs):
        if not self.is_allowed(request):
            return HttpResponseForbidden()

        entry = get_object_or_404(
            self.model_class, id=id
        )

        form = self.form_class(
            request.POST,
            instance=entry
        )
        change_url = reverse(
            self.change_url, args=(id,)
        )

        if form.is_valid():
            form.save()
            return redirect(self.list_url)

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'action_url': change_url,
                'title': self.title
            }
        )


@method_decorator(login_required, name='dispatch')
class AdminView(CommonView):
    """
    View/Create new entry
    """

    def get(self, request, **kwargs):
        if not self.is_allowed(request):
            return HttpResponseForbidden()

        form = self.form_class(
            user = request.user
        )
        action_url = reverse(self.action_url)

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'action_url': action_url,
                'title': self.title
            }
        )

    def post(self, request, **kwargs):
        if not self.is_allowed(request):
            return HttpResponseForbidden()

        form = self.form_class(
            request.POST,
            user = request.user
        )
        if form.is_valid():
            # When saving a form with commit=False option you
            # need to call save_m2m() on the form
            # after you save the object, just as you would for a
            # form with normal many to many fields on
            # it.
            obj = form.save(commit=False)
            if request.user:
                if hasattr(obj, 'user'):
                    obj.user = request.user

            # save object regardles if it has user attribute.
            obj.save()
            form.save_m2m()

            return redirect(self.list_url)

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'action_url': self.action_url,
                'title': self.title
            }
        )


@method_decorator(login_required, name='dispatch')
class AdminListView(CommonView):
    """
    List entries (with pagination)
    """

    def render_with_pagination(self, request, page_number):
        objs = self.get_queryset(request)

        paginator = Paginator(objs, per_page=25)
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

        return render(
            request,
            self.template_name,
            {
                'object_list': page_obj.object_list,
                'pages': pages,
                'page_number': page_number,
                'page': page_obj,
                'list_url': self.list_url
            }
        )

    def post(self, request, *args, **kwargs):
        if not self.is_allowed(request):
            return HttpResponseForbidden()

        selected_action = request.POST.getlist('_selected_action')
        go_action = request.POST['action']
        if go_action == 'delete_selected':
            deleted, row_count = self.model_class.objects.filter(
                id__in=selected_action
            ).delete()

            if deleted:
                count = row_count[self.model_label]

                if count == 1:
                    name = self.model_class._meta.verbose_name
                else:
                    name = self.model_class._meta.verbose_name_plural

                msg_sg = "%(count)s %(name)s was successfully deleted."
                msg_pl = "%(count)s %(name)s were successfully deleted."
                messages.info(
                    request,
                    ngettext(msg_sg, msg_pl, count) % {
                        'count': count,
                        'name': name
                    }
                )

        page_number = int(request.GET.get('page', 1))

        return self.render_with_pagination(
            request,
            page_number
        )

    def get(self, request, *args, **kwargs):
        if not self.is_allowed(request):
            return HttpResponseForbidden()

        page_number = int(request.GET.get('page', 1))

        return self.render_with_pagination(
            request,
            page_number
        )
