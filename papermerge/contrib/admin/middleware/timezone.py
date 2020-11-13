import pytz

from django.utils import timezone


class TimezoneMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        preferences = request.user.preferences
        tzname = preferences['localization__timezone']

        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
