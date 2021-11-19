# Importing shared resources (Inheritances)
from Bluedit.share.Generator import Generator
from Bluedit.share.Sanitizer import Sanitizer
from Bluedit.share.Email import Email
from Bluedit.share.OTP import OTP

# Importing Account table gateway
from Bluedit.post.post_gateway import PostGateway
from Bluedit.home.home_gateway import HomeGateway
from Bluedit.admin.admin_gateway import AdminGateway

import os
import html
from Bluedit.post.models.Post import Post
from Bluedit.post.models.Reply import Reply


class PostManager(Generator, Sanitizer, Email, OTP):
    def __init__(self):
        self.gateway = PostGateway()
        self.admin_gateway = AdminGateway()
        self.home_gateway = HomeGateway()

    def delete_post(self, postid):
        result = self.gateway.delete_post(postid)

        if isinstance(result, str):
            return -1
        else:
            return result

    def delete_reply(self, replyid):
        result = self.gateway.delete_reply(replyid)

        if isinstance(result, str):
            return -1
        else:
            return result

    def add_image_to_folder(self, parent_path, filename, image):
        path = parent_path + filename
        counter = 1

        while os.path.isfile(path):
            path = parent_path + str(counter) + "_" + filename
            counter += 1

        image.save(path)
        return path

    def upload_post(self, title, content, cat, path, id):
        post = Post(self.generate_id(), title, content, self.generate_time(), 0, 0, 0, path, 1, 0, cat, id)
        result = self.gateway.insert_post(post)

        if isinstance(result, str):
            return -1
        else:
            return post.postID

    def get_post(self, id):
        data = self.gateway.select_post_by_id(id)

        if isinstance(data, str):
            return -1
        elif not data[0]:
            return -2

        post, cat = data[0][0], data[1]

        tmp = Post(post[0], post[1], html.unescape(post[2]), post[3].strftime('%Y-%m-%d %H:%M:%S'), post[4],
                   post[5], post[6], post[7], post[8], post[9], [], post[12])
        tmp_cat = [item[0] for item in cat if item[1] == post[0]]
        tmp.postCat = tmp_cat

        return tmp

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

    def get_postlock_status(self, postid):
        data = self.admin_gateway.select_lockstatus_by_id(postid)

        if isinstance(data, str):
            return -1
        elif not data:
            return -2
        return data[0][0]

    def get_replies(self, post_id):
        data = self.gateway.select_replies_by_postid(post_id)
        replies = []

        if isinstance(data, str):
            return -1
        elif not data:
            return -2

        for r in data:
            reply = Reply(r[0], html.unescape(r[1]), r[2], r[3], r[4], r[5], r[8])
            replies.append(reply)

        return replies

    def upload_comments(self, post_id, user_id, comment):
        reply_id = self.generate_id()
        result = self.gateway.insert_replies(post_id, user_id, comment, self.generate_time(), reply_id)

        if isinstance(result, str):
            return -1
        else:
            return reply_id

    def get_reply_by_replyid(self, reply_id):
        data = self.gateway.select_reply_by_replyid(reply_id)

        if isinstance(data, str):
            return -1
        elif not data:
            return -2

        i = data[0]
        tmp = [i[0], html.unescape(i[1]), i[2], i[3].strftime('%Y-%m-%d %H:%M:%S'), i[5], i[8],
               html.unescape(i[9]), i[19]]

        return tmp

    def update_reply(self, reply_id, content):
        result = self.gateway.update_reply(reply_id, content)

        if isinstance(result, str):
            return -1
        else:
            return result

    def check_reply_exist(self, reply_id):
        result = self.gateway.select_exist_reply_by_id(reply_id)

        if isinstance(result, str):
            return -1
        else:
            return result[0]

    def check_reply_report_list(self, replyid, userid):
        result = self.gateway.select_exist_reply_reportuser(replyid, userid)

        if isinstance(result, str):
            return -1
        elif result[0] == 1:
            return True
        else:
            return False

    def report_reply(self, replyid, userid):
        result = self.gateway.insert_reportedreply(replyid, userid)

        if isinstance(result, str):
            return -1
        else:
            return result

    def get_rlike_stash(self, reply_id):
        data = self.gateway.select_rlike_by_id(reply_id)

        if isinstance(data, str):
            return -1
        else:
            return data

    def like_reply(self, reply_id, user_id):
        result = self.gateway.update_reply_like_increment(reply_id, user_id)

        if isinstance(result, str):
            return -1
        else:
            return result

    def unlike_reply(self, reply_id, user_id):
        result = self.gateway.update_reply_like_decrement(reply_id, user_id)

        if isinstance(result, str):
            return -1
        else:
            return result

    def check_reply_is_mine(self, replyid, userid):
        result = self.gateway.select_exist_reply_is_mine(replyid, userid)

        if isinstance(result, str):
            return -1
        else:
            return result[0]

    def delete_reply_by_id(self, replyid, userid):
        result = self.gateway.delete_reply_by_id(replyid, userid)

        if isinstance(result, str):
            return -1
        else:
            return result

    def update_post(self, postid, title, content):
        result = self.gateway.update_post(postid, title, content)

        if isinstance(result, str):
            return -1
        else:
            return result

    def check_post_exist(self, post_id):
        result = self.gateway.select_exist_post_by_id(post_id)

        if isinstance(result, str):
            return -1
        else:
            return result[0]

    def check_report_list(self, postid, userid):
        result = self.gateway.select_exist_reportuser(postid, userid)

        if isinstance(result, str):
            return -1
        elif result[0] == 1:
            return True
        else:
            return False

    def report_post(self, postid, userid):
        result = self.gateway.insert_reportedpost(postid, userid)

        if isinstance(result, str):
            return -1
        else:
            return result

    def get_like_list(self, post_id):
        data = self.gateway.select_like_by_id(post_id)

        if isinstance(data, str):
            return -1
        else:
            return data

    def like_post(self, post_id, user_id):
        result = self.gateway.update_post_like_increment(post_id, user_id)

        if isinstance(result, str):
            return -1
        else:
            return result

    def dislike_post(self, post_id, user_id):
        result = self.gateway.update_post_like_decrement(post_id, user_id)

        if isinstance(result, str):
            return -1
        else:
            return result

    def get_save_stash(self, post_id):
        data = self.gateway.select_saved_by_id(post_id)

        if isinstance(data, str):
            return -1
        else:
            return data

    def save_post(self, post_id, user_id):
        result = self.gateway.update_post_save_increment(post_id, user_id)

        if isinstance(result, str):
            return -1
        else:
            return result

    def unsave_post(self, post_id, user_id):
        result = self.gateway.update_post_save_decrement(post_id, user_id)

        if isinstance(result, str):
            return -1
        else:
            return result

    def check_post_is_mine(self, postid, userid):
        result = self.gateway.select_exist_post_is_mine(postid, userid)

        if isinstance(result, str):
            return -1
        else:
            return result[0]

    def delete_post_by_id(self, postid, userid):
        result = self.gateway.delete_post_by_id(postid, userid)

        if isinstance(result, str):
            return -1
        else:
            return result
