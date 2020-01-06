from django.conf import settings


def static_bundle_url(request):
    """
    Static resources are deployed separately from main django app
    and are available via /webassets/ prefix.

    In production static resources are also versioned.
    """
    if settings.DEBUG:
        path_js = "/papermerge-assets/static/js/all.js"
        path_css = "/papermerge-assets/static/css/all.css"
        oxygen_path_js = "/oxygen-assets/static/js/all.js"
        oxygen_path_css = "/oxygen-assets/static/css/all.css"
    else:
        path_js = "/papermerge-assets/static/js/all.{}.js".format(
            settings.papermerge_ASSETS_VER
        )
        path_css = "/papermerge-assets/static/css/all.{}.css".format(
            settings.papermerge_ASSETS_VER
        )
        oxygen_path_js = "/oxygen-assets/static/js/all.{}.js".format(
            settings.OXYGEN_ASSETS_VER
        )
        oxygen_path_css = "/oxygen-assets/static/css/all.{}.css".format(
            settings.OXYGEN_ASSETS_VER
        )

    return {
        'papermerge_JS_URL': path_js,
        'papermerge_CSS_URL': path_css,
        'OXYGEN_JS_URL': oxygen_path_js,
        'OXYGEN_CSS_URL': oxygen_path_css,
    }
