import logging


logger = logging.getLogger(__name__)


class VirtualMailbox:

    def __init__(self, connection):
        self._connection = connection

    @property
    def connection(self):
        return self._connection

    def build_email(self, username, company, domain):
        return f"{username}@{company}.{domain}"

    def user_add(self, username, password, company, domain):
        email = self.build_email(
            username,
            company,
            domain
        )

        with self.connection.cursor() as cursor:
            cursor.callproc(
                "dgl_add_user",
                [email, password]
            )

    def user_exists(self, email):
        """
        check that user with given email mailbox exists in DB
        """
        pass

    def user_delete(self, username, company, domain):
        email = self.build_email(
            username,
            company,
            domain
        )
        with self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM virtual_users WHERE virtual_mailbox = %s",
                [email]
            )
