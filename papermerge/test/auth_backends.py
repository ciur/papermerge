from django.contrib.auth import get_user_model


class TestcaseUserBackend(object):
    """
    Custom authentication backend which... well, skips
    authentication. Very usefull for testing views functionality
    where authentication is not on in primary focus.
    """

    def authenticate(self, request, testcase_user=None):
        return testcase_user

    def get_user(self, user_id):
        User = get_user_model()
        user = User.objects.get(pk=user_id)
        return user
