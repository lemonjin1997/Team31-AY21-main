# Importing shared resources (Inheritances)
from Bluedit.share.Generator import Generator
from Bluedit.share.Sanitizer import Sanitizer
from Bluedit.share.Email import Email
from Bluedit.share.OTP import OTP

# Importing Account table gateway
from Bluedit.home.home_gateway import HomeGateway
from Bluedit.post.models.Post import Post

import html


class HomeManager(Generator, Sanitizer, Email, OTP):
    def __init__(self):
        self.gateway = HomeGateway()

    def get_all_post(self):
        data = self.gateway.get_all_post()
        posts, cat = data[0], data[1]
        post_list = []

        if isinstance(data, str): return -1

        for post in posts:
            tmp = Post(post[0], post[1], html.unescape(post[2]), post[3].strftime('%Y-%m-%d %H:%M:%S'), post[4],
                       post[5], post[6], post[7], post[8], post[9], [], post[12])
            tmp_cat = [item[0] for item in cat if item[1] == post[0]]
            tmp.postCat = tmp_cat
            post_list.append(tmp)

        return post_list

    def get_like_list_by_userid(self, userid):
        data = self.gateway.select_like_by_userid(userid)
        lst = []

        if isinstance(data, str):
            return -1
        else:
            if not data:
                return lst
            else:
                for item in data:
                    lst.append(item[0])
                return lst

    def get_save_list_by_userid(self, userid):
        data = self.gateway.select_save_by_userid(userid)
        lst = []

        if isinstance(data, str):
            return -1
        else:
            if not data:
                return lst
            else:
                for item in data:
                    lst.append(item[0])
                return lst