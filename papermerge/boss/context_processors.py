from django.conf import settings


def static_bundle_url(request):
    """
    Static resources are deployed separately from main django app
    and are available via /assets/ prefix.

    In production static resources are also versioned.
    """
    if settings.DEBUG:
        path_js = f"{settings.STATIC_URL}js/papermerge.js"
        path_css = f"{settings.STATIC_URL}css/papermerge.css"
    else:
        ver = settings.ASSETS_VER or ""
        path_js = f"{settings.STATIC_URL}js/papermerge.{ver}.js"
        path_css = f"{settings.STATIC_URL}css/papermerge.{ver}.css"

    return {
        'JS_URL': path_js,
        'CSS_URL': path_css,
    }
