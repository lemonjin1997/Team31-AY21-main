from operator import attrgetter


class PostSort:
    def select_sort_method(self, sort_id, post_collection):
        if sort_id == "1":
            return self.sort_latestPost(post_collection)
        elif sort_id == "2":
            return self.sort_oldestPost(post_collection)
        elif sort_id == "3":
            return self.sort_mostFav(post_collection)
        elif sort_id == "4":
            return self.sort_leastFav(post_collection)
        elif sort_id == "5":
            return self.sort_mostComment(post_collection)
        elif sort_id == "6":
            return self.sort_leastComment(post_collection)
        elif sort_id == "7":
            return self.sort_mostSaves(post_collection)
        elif sort_id == "8":
            return self.sort_leastSaves(post_collection)
        else:
            return -1

    def sort_latestPost(self, posts):
        posts.sort(key=attrgetter('postTime'), reverse=True)
        return posts

    def sort_oldestPost(self, posts):
        posts.sort(key=attrgetter('postTime'))
        return posts

    def sort_mostFav(self, posts):
        posts.sort(key=attrgetter('postLikes'), reverse=True)
        return posts

    def sort_leastFav(self, posts):
        posts.sort(key=attrgetter('postLikes'))
        return posts

    def sort_mostComment(self, posts):
        posts.sort(key=attrgetter('postReplies'), reverse=True)
        return posts

    def sort_leastComment(self, posts):
        posts.sort(key=attrgetter('postReplies'))
        return posts

    def sort_mostSaves(self, posts):
        posts.sort(key=attrgetter('postSaves'), reverse=True)
        return posts

    def sort_leastSaves(self, posts):
        posts.sort(key=attrgetter('postSaves'))
        return posts
