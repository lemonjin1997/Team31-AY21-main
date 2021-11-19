# Importing shared resources (Inheritances)
import html

from Bluedit.share.Generator import Generator
from Bluedit.share.Sanitizer import Sanitizer
from Bluedit.share.Email import Email
from Bluedit.share.OTP import OTP

from Bluedit.admin.admin_gateway import AdminGateway


class AdminManager(Generator, Sanitizer, Email, OTP):
    def __init__(self):
        self.gateway = AdminGateway()

    def get_user(self):
        data = self.gateway.select_all_user()

        if isinstance(data, str):
            return -1
        elif not data:
            return False
        else:
            return data

    def promote_user(self, user_id):
        result = self.gateway.update_userrole_by_id(user_id)

        if isinstance(result, str):
            return -1
        else:
            return True

    def get_reported_post(self):
        data = self.gateway.select_reported_post_list()
        reported_list = []

        if isinstance(data, str):
            return -1
        elif not data:
            return False
        else:
            for item in data:
                tmp = [item[0], item[1], html.unescape(item[2]), item[3]]
                reported_list.append(tmp)

            return reported_list

    def get_locked_post(self):
        data = self.gateway.select_locked_post()

        if isinstance(data, str):
            return -1
        elif not data:
            return False
        else:
            return data

    def check_post_lock_status(self, postid):
        data = self.gateway.select_lockstatus_by_id(postid)

        if isinstance(data, str):
            return -1
        elif not data:
            return -2
        elif data[0][0] == 1:
            return True
        else:
            return False

    def lock_post(self, postid):
        result = self.gateway.update_postlock(postid)

        if isinstance(result, str):
            return -1
        else:
            return result

    def unlock_post(self, postid):
        result = self.gateway.update_postlock_unlock(postid)

        if isinstance(result, str):
            return -1
        else:
            return result

    def get_reported_reply(self):
        data = self.gateway.select_reported_reply_list()
        reported_list = []

        if isinstance(data, str):
            return -1
        elif not data:
            return False
        else:
            for item in data:
                tmp = [item[0], html.unescape(item[1]), item[2]]
                reported_list.append(tmp)

            return reported_list

    def get_all_user(self):
        data = self.gateway.select_all_user_by_auth()

        if isinstance(data, str):
            return -1
        elif not data:
            return False
        else:
            return data

    def get_ban_list(self):
        data = self.gateway.select_banned_userid()

        if isinstance(data, str):
            return -1
        elif not data:
            return False
        else:
            return data

    def check_ban_status(self, userid):
        data = self.gateway.select_banstatus_by_id(userid)

        if isinstance(data, str):
            return -1
        elif not data:
            return -2
        elif data[0][0] == 1:
            return False
        else:
            return True

    def ban_user(self, userid):
        result = self.gateway.update_user_accStatus(userid)

        if isinstance(result, str):
            return -1
        else:
            return result

    def unban_user(self, userid):
        result = self.gateway.update_user_accStatus_unban(userid)

        if isinstance(result, str):
            return -1
        else:
            return result