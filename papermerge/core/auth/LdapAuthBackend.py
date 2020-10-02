from django_auth_ldap.backend import LDAPBackend


class LdapAuthBackend(LDAPBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        return super(LdapAuthBackend, self).authenticate(request, username, password, **kwargs)

    def get_user(self, user_id):
        return super(LdapAuthBackend, self).get_user(user_id)
