import pytz

from django.utils import timezone


class TimezoneMiddleware:
    """
    User preferences override l10n configuration from settings file.

    Per project (django project level) configurations are set in
    settings file (config.settings.*). Localization preferences
    i.e. for date & time format, timezone can be overridden by user.

    This middleware activates timezone considering user preferences.

    User preferences are set via:
        Admin -> Preferences -> Localization -> Timezone
    configuration.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # user preferences make sense only
        # in case of authenticated user
        if request.user.is_anonymous:
            return self.get_response(request)

        preferences = request.user.preferences
        tzname = preferences['localization__timezone']

        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()

        return self.get_response(request)
