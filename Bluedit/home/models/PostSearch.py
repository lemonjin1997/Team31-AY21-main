# Importing shared resources (Inheritances)
from Bluedit.share.Sanitizer import Sanitizer

# Importing Account table gateway
from Bluedit.home.home_gateway import HomeGateway
from Bluedit.post.models.Post import Post

import html


class PostSearch(Sanitizer):
    def __init__(self):
        self.gateway = HomeGateway()

    def select_search_method(self, target, value):
        if target == "postTitle":
            result = self.search_postTitle(target, value)
        elif target == "postContent":
            result = self.search_postContent(target, value)
        elif target == "UUID":
            result = self.search_UUID(value)
        elif target == "postCat":
            result = self.search_postCat(value)
        else:
            result = None

        return result

    def search_postTitle(self, target, value):
        data = self.gateway.get_all_post_with_conditions(target, value)
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

    def search_postContent(self, target, value):
        value = self.validate_text_replaceSymbol(value)
        data = self.gateway.get_all_post_with_conditions(target, value)
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

    def search_UUID(self, value):
        data = self.gateway.get_all_post_with_conditions("username", value)
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

    def search_postCat(self, value):
        data = self.gateway.get_all_post()
        posts, cat = data[0], data[1]
        post_list = []

        if isinstance(data, str): return -1

        for post in posts:
            tmp = Post(post[0], post[1], html.unescape(post[2]), post[3].strftime('%Y-%m-%d %H:%M:%S'), post[4],
                       post[5], post[6], post[7], post[8], post[9], [], post[12])
            tmp_cat = [item[0] for item in cat if item[1] == post[0]]

            if value not in tmp_cat:
                continue
            else:
                tmp.postCat = tmp_cat
                post_list.append(tmp)

        return post_list
