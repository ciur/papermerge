import os
import subprocess
import logging
from subprocess import Popen

logger = logging.getLogger(__name__)


class SFTPUsers:
    """
    System sftp users name (which are usual unix account users)
    have format:

        <prefix><company_name>_<web_username>

    Examples:
        Company opel with two web users: opeladmin
        and xyz1 and given prefix is sftp_ will have
        following unix accounts:

            * sftp_opel_opeladmin
            * sftp_opel_xyz1

    This way unique unix users per tenant are guaranteed.
    """

    def __init__(self, prefix, company, gname):
        self._gname = gname
        self._company = company
        self._prefix = prefix

    def group_add(self):
        args = ["groupadd", "-f", self._gname]
        logger.debug(args)
        self.call(args)

    def prefixed(self, uname):
        username = f"{self._prefix}{self._company}_{uname}"
        return username

    def add(self, username, pw):
        self.user_add(username)
        self.mkdirs(username)
        self.passwd(username, pw)

    def user_exists(self, uname):
        username = self.prefixed(uname)
        return os.path.exists(
            f"/home/{username}"
        )

    def user_add(self, uname):
        """
        creates a user with prefix self._prefix. User belongs to
        the self._gname group.
        """
        # create group if it does not exist
        self.group_add()
        username = self.prefixed(uname)
        args = [
            "useradd",
            "-g",
            self._gname,
            "-d",
            "/home/{}".format(username),
            "-s",
            "/sbin/nologin",
            username
        ]
        logger.debug(args)
        self.call(args)

    def mkdirs(self, uname):
        username = self.prefixed(uname)
        home_dir = "/home/{}".format(username)
        upload_dir = "/home/{}/upload".format(username)
        arr = [
            ["mkdir", "-p", home_dir],
            ["chown", "root:root", home_dir],
            ["chmod", "755", home_dir],
            ["mkdir", "-p", upload_dir],
            ["chown", "{}:{}".format(username, self._gname), upload_dir]
        ]
        for args in arr:
            logger.debug(args)
            self.call(args)

    def passwd(self, uname, pw):
        """
        Set (sftp) password pw for system user uname.

        pw might be empty: initially when user is created
        his userprofile is created with both sftp_passwd1
        and sftp_passwd2 empty. Then a django signal is sent
        to user model and update it - and that update triggers
        this method - with pw empty.

        The idea is that users have sftp account disabled by default.
        They need to enabled it in user profile. When users
        update their user profile this method is triggered with
        pw - non empty.
        """
        username = self.prefixed(uname)
        if not pw:
            logger.info(
                f"sftp_user {uname} disabled."
            )
            return

        logger.debug(
            "Changing password for local user={}".format(username)
        )
        proc = Popen(
            ['/usr/bin/passwd', username],
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE

        )
        proc.stdin.write(
            bytes(pw + "\n", encoding='utf-8')
        )
        proc.stdin.write(
            bytes(pw, encoding='utf-8')
        )
        proc.stdin.flush()
        stdout, stderr = proc.communicate()

        logger.debug(f"stdout={stdout} stderr={stderr}")

    def call(self, args):
        subprocess.call(args)
