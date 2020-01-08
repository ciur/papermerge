from django.conf import settings


def static_bundle_url(request):
    """
    Static resources are deployed separately from main django app
    and are available via /assets/ prefix.

    In production static resources are also versioned.
    """
    if settings.DEBUG:
        path_js = "/assets/static/js/all.js"
        path_css = "/assets/static/css/all.css"
    else:
        ver = settings.ASSETS_VER or ""
        path_js = f"/assets/static/js/all.{ver}.js"
        path_css = f"/assets/static/css/all.{ver}.css"

    return {
        'JS_URL': path_js,
        'CSS_URL': path_css,
    }
