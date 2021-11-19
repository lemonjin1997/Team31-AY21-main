# Importing shared resources (Inheritances)
import os
import shutil

from Bluedit.share.Generator import Generator
from Bluedit.share.Sanitizer import Sanitizer
from Bluedit.share.Email import Email
from Bluedit.share.OTP import OTP

# Importing Account table gateway
from Bluedit.profile.profile_gateway import ProfileGateway
from Bluedit.home.home_gateway import HomeGateway
from Bluedit.profile.models.Profile import Profile
from Bluedit.post.models.Post import Post

import html


class ProfileManager(Generator, Sanitizer, Email, OTP):
    def __init__(self):
        self.gateway = ProfileGateway()
        self.home_gateway = HomeGateway()

    def name_exist(self, name):
        result = self.gateway.select_exist_name(name)

        if isinstance(result, str):
            return -1
        elif result[0] == 1:
            return True
        else:
            return False

    def get_profile(self, name):
        data = self.gateway.select_profile_by_name(name)

        if isinstance(data, str):
            return -1
        elif not data:
            return -2
        else:
            profile = Profile(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
            return profile

    def get_user_post_top_3(self, name):
        data = self.gateway.select_top3user_post_by_name(name)
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

    def set_profile_image_folder(self, path, image, filename):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                os.makedirs(path)
                image.save(path + "/" + filename)
            else:
                os.makedirs(path)
                image.save(path + "/" + filename)

            return True
        except:
            return False

    def update_user_image_path(self, path, name, id):
        result = self.gateway.update_image_by_nameid(path, name, id)

        if isinstance(result, str):
            return -1
        else:
            return result

    def get_user_fa_status(self, id):
        data = self.gateway.select_fa_by_id(id)

        if isinstance(data, str):
            return -1
        else:
            return data[0]

    def update_username(self, cur_name, input_name, id):
        result = self.gateway.update_name_by_nameid(cur_name, input_name, id)

        if isinstance(result, str):
            return -1
        else:
            return result

    def update_about(self, name, id, about):
        result = self.gateway.update_about_by_nameid(name, id, about)

        if isinstance(result, str):
            return -1
        else:
            return result

    def get_user_post(self, name):
        data = self.gateway.select_user_post_by_name(name)
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

    def get_stashed_post(self, id):
        data = self.gateway.select_stashed_post_by_id(id)
        posts, cat = data[0], data[1]
        post_list = []

        if isinstance(data, str): return -1

        for post in posts:
            tmp = Post(post[3], post[4], html.unescape(post[5]), post[6].strftime('%Y-%m-%d %H:%M:%S'), post[7],
                       post[8], post[9], post[10], post[11], post[12], [], post[15])
            tmp_cat = [item[0] for item in cat if item[1] == post[3]]
            tmp.postCat = tmp_cat
            post_list.append(tmp)

        return post_list

    def get_like_list_by_userid(self, userid):
        data = self.home_gateway.select_like_by_userid(userid)
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
        data = self.home_gateway.select_save_by_userid(userid)
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

    def get_upvote_post(self, id):
        data = self.gateway.select_upvote_post_by_id(id)
        posts, cat = data[0], data[1]
        post_list = []

        if isinstance(data, str): return -1

        for post in posts:
            tmp = Post(post[3], post[4], html.unescape(post[5]), post[6].strftime('%Y-%m-%d %H:%M:%S'), post[7],
                       post[8], post[9], post[10], post[11], post[12], [], post[15])
            tmp_cat = [item[0] for item in cat if item[1] == post[3]]
            tmp.postCat = tmp_cat
            post_list.append(tmp)

        return post_list

    def get_upvote_reply(self, id):
        data = self.gateway.select_upvoted_reply_by_id(id)
        reply_list = []

        if isinstance(data, str):
            return -1

        for i in data:
            tmp = [i[3], html.unescape(i[4]), i[5], i[6].strftime('%Y-%m-%d %H:%M:%S'), i[8], i[11], html.unescape(i[12]), i[22]]
            reply_list.append(tmp)

        return reply_list

    def get_r_like_list_by_userid(self, userid):
        data = self.home_gateway.select_r_like_by_userid(userid)
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

    def get_commented_post(self, id):
        data = self.gateway.select_commented_post_by_id(id)
        reply_list = []

        if isinstance(data, str):
            return -1

        for i in data:
            tmp = [i[0], html.unescape(i[1]), i[2], i[3].strftime('%Y-%m-%d %H:%M:%S'), i[8], html.unescape(i[9]), i[5], i[19]]
            reply_list.append(tmp)

        return reply_list