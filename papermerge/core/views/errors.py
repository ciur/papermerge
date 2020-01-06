from django.views import defaults


def bad_request_400_custom(
    request,
    exception,
    template_name='core/400.html'
):
    return defaults.bad_request(
        request=request,
        exception=exception,
        template_name=template_name
    )


def permission_denied_403_custom(
        request,
        exception,
        template_name='core/403.html'
):
    return defaults.permission_denied(
        request=request,
        exception=exception,
        template_name=template_name
    )


def page_not_found_404_custom(
    request,
    exception,
    template_name='core/404.html'
):
    return defaults.page_not_found(
        request=request,
        exception=exception,
        template_name=template_name
    )


def server_error_500_custom(
    request,
    template_name='core/500.html'
):
    return defaults.server_error(
        request=request,
        template_name=template_name
    )
