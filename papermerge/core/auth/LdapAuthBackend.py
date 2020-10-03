import logging
from papermerge.core.models import UserAuthenticationSource

logger = logging.getLogger(__name__)

try:
    from django_auth_ldap.backend import LDAPBackend

    class LdapAuthBackend(LDAPBackend):
        def authenticate(self, request, username=None, password=None, **kwargs):
            return super(LdapAuthBackend, self).authenticate(request, username, password, **kwargs)

        def get_user(self, user_id):
            user = super(LdapAuthBackend, self).get_user(user_id)
            user.authentication_source = UserAuthenticationSource.LDAP
            return user

except ModuleNotFoundError as e:
    # As some required module for LDAP was not installed we need to return the authentication that logs warnings that LDAP is disabled.
    class LdapAuthBackend:
        def authenticate (self):
            logger.warning("LDAP authentication is disabled but set up to be used within the configuration.")
            return None

        def get_user (self, user_id):
            logger.warning("LDAP authentication is disabled but set up to be used within the configuration.")
            return None