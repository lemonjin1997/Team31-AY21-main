# Importing shared resources (Inheritances)
from Bluedit.api import mysql
from Bluedit.log import error_logger


class PostGateway:
    def delete_post(self, postid):
        query_like_list = """SELECT UUID FROM post_favourite WHERE PostID = %s"""
        tuple_like_list = (postid,)

        query_save_list = """SELECT UUID FROM user_stash WHERE PostID = %s"""
        tuple_save_list = (postid,)

        query_report_list = """SELECT UUID FROM post_blacklist WHERE PostID = %s"""
        tuple_report_list = (postid,)

        query_reply_list = """SELECT ReplyID, UUID FROM reply WHERE PostID = %s"""
        tuple_reply_list = (postid,)

        query_remove_like = """DELETE FROM post_favourite WHERE PostID = %s"""
        tuple_remove_like = (postid,)

        query_remove_save = """DELETE FROM user_stash WHERE PostID = %s"""
        tuple_remove_save = (postid,)

        query_remove_reported = """DELETE FROM post_blacklist WHERE PostID = %s"""
        tuple_remove_reported = (postid,)

        query_remove_post = """UPDATE post SET postStatus = %s WHERE PostID = %s"""
        tuple_remove_post = (0, postid)

        query_get_user = """SELECT UUID FROM post WHERE PostID = %s"""
        tuple_get_user = (postid,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_like_list, tuple_like_list)
            like_list = cursor.fetchall()

            cursor.execute(query_remove_like, tuple_remove_like)
            for like in like_list:
                query_decrement_like = """UPDATE profile SET upvoted = (upvoted - %s)  WHERE UUID = %s"""
                tuple_decrement_like = (1, like[0])
                cursor.execute(query_decrement_like, tuple_decrement_like)

            cursor.execute(query_save_list, tuple_save_list)
            save_list = cursor.fetchall()

            cursor.execute(query_remove_save, tuple_remove_save)
            for save in save_list:
                query_decrement_save = """UPDATE profile SET saved = (saved - %s)  WHERE UUID = %s"""
                tuple_decrement_save = (1, save[0])
                cursor.execute(query_decrement_save, tuple_decrement_save)

            cursor.execute(query_report_list, tuple_report_list)
            report_list = cursor.fetchall()

            cursor.execute(query_remove_reported, tuple_remove_reported)
            for report in report_list:
                query_decrement_report = """UPDATE profile SET reported = (reported - %s)  WHERE UUID = %s"""
                tuple_decrement_report = (1, report[0])
                cursor.execute(query_decrement_report, tuple_decrement_report)

            cursor.execute(query_reply_list, tuple_reply_list)
            reply_list = cursor.fetchall()

            for reply in reply_list:
                query_reply_like_list = """SELECT UUID FROM reply_favourite WHERE ReplyID = %s"""
                tuple_reply_like_list = (reply[0],)
                cursor.execute(query_reply_like_list, tuple_reply_like_list)
                reply_like_list = cursor.fetchall()

                for reply_like in reply_like_list:
                    query_decrement_reply_like = """UPDATE profile SET upvoted = (upvoted - %s)  WHERE UUID = %s"""
                    tuple_decrement_reply_like = (1, reply_like[0])
                    cursor.execute(query_decrement_reply_like, tuple_decrement_reply_like)

                query_remove_commented = """UPDATE profile SET commented = (commented - %s) WHERE UUID = %s"""
                tuple_remove_commented = (1, reply[1])
                cursor.execute(query_remove_commented, tuple_remove_commented)

                query_remove_reply = """UPDATE reply SET replyStatus = %s WHERE ReplyID = %s"""
                tuple_remove_reply = (0, reply[0])
                cursor.execute(query_remove_reply, tuple_remove_reply)

            cursor.execute(query_remove_post, tuple_remove_post)

            cursor.execute(query_get_user, tuple_get_user)
            user = cursor.fetchone()

            query_decrement_posted = """UPDATE profile SET posted  = (posted - %s) WHERE UUID = %s"""
            tuple_decrement_posted = (1, user[0])
            cursor.execute(query_decrement_posted, tuple_decrement_posted)

            conn.commit()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def delete_reply(self, replyid):
        query_like_list = """SELECT UUID FROM reply_favourite WHERE ReplyID = %s"""
        tuple_like_list = (replyid,)

        query_report_list = """SELECT UUID FROM reply_blacklist WHERE ReplyID = %s"""
        tuple_report_list = (replyid,)

        query_get_post = """SELECT PostID FROM reply WHERE ReplyID = %s"""
        tuple_get_post = (replyid,)

        query_remove_list = """DELETE FROM reply_favourite WHERE ReplyID = %s"""
        tuple_remove_list = (replyid,)
        query_remove_reported = """DELETE FROM reply_blacklist WHERE ReplyID = %s"""
        tuple_remove_reported = (replyid,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_like_list, tuple_like_list)
            like_list = cursor.fetchall()

            cursor.execute(query_remove_list, tuple_remove_list)
            for like in like_list:
                query_decrement_like = """UPDATE profile SET upvoted = (upvoted - %s)  WHERE UUID = %s"""
                tuple_decrement_like = (1, like[0])
                cursor.execute(query_decrement_like, tuple_decrement_like)

            cursor.execute(query_report_list, tuple_report_list)
            report_list = cursor.fetchall()

            cursor.execute(query_remove_reported, tuple_remove_reported)
            for report in report_list:
                query_decrement_like = """UPDATE profile SET reported = (reported - %s)  WHERE UUID = %s"""
                tuple_decrement_like = (1, report[0])
                cursor.execute(query_decrement_like, tuple_decrement_like)

            cursor.execute(query_get_post, tuple_get_post)
            post = cursor.fetchall()

            for i in post:
                query_decrement_replies = """UPDATE post SET postReplies = (postReplies - %s) WHERE PostID = %s"""
                tuple_decrement_replies = (1, i[0])
                cursor.execute(query_decrement_replies, tuple_decrement_replies)

            query_user = """SELECT UUID FROM reply WHERE ReplyID = %s"""
            tuple_user = (replyid,)
            cursor.execute(query_user, tuple_user)
            user = cursor.fetchone()

            query_decrement_commented = """UPDATE profile SET commented = (commented - %s) WHERE UUID = %s"""
            tuple_decrement_commented = (1, user[0])
            cursor.execute(query_decrement_commented, tuple_decrement_commented)

            query_delete_reply = """UPDATE reply SET replyStatus = %s WHERE ReplyID = %s"""
            tuple_delete_reply = (0, replyid)
            cursor.execute(query_delete_reply, tuple_delete_reply)

            conn.commit()
            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def insert_post(self, post):
        query_post = """INSERT INTO post VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        tuple_post = (
            post.postID, post.postTitle, post.postContent, post.postTime, post.postLikes, post.postReplies,
            post.postSaves,
            post.postImage, post.postStatus, post.postLock, post.UUID)

        query_update_profile = """UPDATE profile SET posted = posted + %s WHERE UUID = %s"""
        tuple_update = (1, post.UUID)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_post, tuple_post)

            for item in post.postCat:
                query_category = """INSERT INTO post_category (CatName, PostID) VALUES (%s, %s)"""
                tuple_cat = (item, post.postID)
                cursor.execute(query_category, tuple_cat)

            cursor.execute(query_update_profile, tuple_update)

            conn.commit()
            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_post_by_id(self, id):
        query_post = """SELECT * FROM post INNER JOIN profile ON post.UUID = profile.UUID WHERE post.PostID = %s and post.postStatus = %s"""
        tuple_post = (id, 1)

        query_category = """SELECT CatName, PostID FROM post_category WHERE PostID = %s"""
        tuple_cat = (id,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_post, tuple_post)
            post = cursor.fetchall()

            cursor.execute(query_category, tuple_cat)
            category = cursor.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return [post, category]

    def select_replies_by_postid(self, postid):
        query_replies = """SELECT * FROM reply INNER JOIN profile ON reply.UUID = profile.UUID WHERE reply.PostID = %s AND reply.replyStatus = %s ORDER BY replyTime DESC"""
        tuple_replies = (postid, 1)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_replies, tuple_replies)
            replies = cursor.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return replies

    def insert_replies(self, post_id, user_id, comment, time, reply_id):
        query_reply = """INSERT INTO reply VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        tuple_reply = (reply_id, comment, post_id, time, 1, 0, user_id)

        query_update_profile = """UPDATE profile SET commented = commented + %s WHERE UUID = %s"""
        tuple_update_profile = (1, user_id)

        query_update_post = """UPDATE post SET postReplies = (postReplies + %s) WHERE PostID = %s"""
        tuple_update_post = (1, post_id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_reply, tuple_reply)
            cursor.execute(query_update_profile, tuple_update_profile)
            cursor.execute(query_update_post, tuple_update_post)

            conn.commit()
            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_reply_by_replyid(self, reply_id):
        query = """SELECT * FROM reply R INNER JOIN post PT ON R.PostID = PT.PostID INNER JOIN profile P ON R.UUID = P.UUID WHERE R.ReplyID = %s AND R.replyStatus = %s"""
        tuple = (reply_id, 1)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def update_reply(self, reply_id, content):
        query = """UPDATE reply SET replyContent = %s WHERE ReplyID = %s AND replyStatus = %s"""
        tuple = (content, reply_id, 1)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            conn.commit()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_exist_reply_by_id(self, reply_id):
        query = """SELECT EXISTS(SELECT * FROM reply WHERE ReplyID = %s AND replyStatus = %s)"""
        tuple = (reply_id, 1)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def select_exist_reply_reportuser(self, replyid, userid):
        query = """SELECT EXISTS(SELECT * FROM reply_blacklist WHERE ReplyID = %s AND UUID = %s)"""
        tuple = (replyid, userid)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def insert_reportedreply(self, replyid, userid):
        query = """INSERT INTO reply_blacklist (ReplyID, UUID) VALUES (%s, %s)"""
        tuple = (replyid, userid)

        query_update = """UPDATE profile SET reported = (reported + %s) WHERE UUID = %s"""
        tuple_update = (1, userid)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            cursor.execute(query_update, tuple_update)
            conn.commit()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_rlike_by_id(self, reply_id):
        query = """SELECT ReplyID, UUID FROM reply_favourite WHERE ReplyID = %s"""
        tuple = (reply_id,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def update_reply_like_increment(self, replyid, userid):
        query_insert_like = """INSERT INTO reply_favourite (ReplyID, UUID) VALUES (%s, %s)"""
        tuple_insert_like = (replyid, userid)

        query_update_profile = """UPDATE profile SET upvoted = (upvoted + %s)  WHERE UUID = %s"""
        tuple_update_profile = (1, userid)

        query_update_post = """UPDATE reply SET replyLikes = (replyLikes + %s) WHERE ReplyID = %s"""
        tuple_update_post = (1, replyid)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_insert_like, tuple_insert_like)
            cursor.execute(query_update_post, tuple_update_post)
            cursor.execute(query_update_profile, tuple_update_profile)

            conn.commit()
            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def update_reply_like_decrement(self, replyid, userid):
        query_delete_like = """DELETE FROM reply_favourite WHERE ReplyID = %s AND UUID = %s"""
        tuple_delete_like = (replyid, userid)

        query_update_profile = """UPDATE profile SET upvoted = (upvoted - %s)  WHERE UUID = %s"""
        tuple_update_profle = (1, userid)

        query_update_post = """UPDATE reply SET replyLikes = (replyLikes - %s) WHERE ReplyID = %s"""
        tuple_update_post = (1, replyid)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_delete_like, tuple_delete_like)
            cursor.execute(query_update_post, tuple_update_post)
            cursor.execute(query_update_profile, tuple_update_profle)

            conn.commit()
            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_exist_reply_is_mine(self, replyid, userid):
        query = """SELECT EXISTS(SELECT * FROM reply WHERE ReplyID = %s AND UUID = %s AND replyStatus = %s)"""
        tuple = (replyid, userid, 1)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def delete_reply_by_id(self, replyid, userid):
        query_like_list = """SELECT UUID FROM reply_favourite WHERE ReplyID = %s"""
        tuple_like_list = (replyid,)

        query_report_list = """SELECT UUID FROM reply_blacklist WHERE ReplyID = %s"""
        tuple_report_list = (replyid,)

        query_get_post = """SELECT PostID FROM reply WHERE ReplyID = %s"""
        tuple_get_post = (replyid,)

        query_remove_list = """DELETE FROM reply_favourite WHERE ReplyID = %s"""
        tuple_remove_list = (replyid,)
        query_remove_reported = """DELETE FROM reply_blacklist WHERE ReplyID = %s"""
        tuple_remove_reported = (replyid,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_like_list, tuple_like_list)
            like_list = cursor.fetchall()

            cursor.execute(query_remove_list, tuple_remove_list)
            for like in like_list:
                query_decrement_like = """UPDATE profile SET upvoted = (upvoted - %s)  WHERE UUID = %s"""
                tuple_decrement_like = (1, like[0])
                cursor.execute(query_decrement_like, tuple_decrement_like)

            cursor.execute(query_report_list, tuple_report_list)
            report_list = cursor.fetchall()

            cursor.execute(query_remove_reported, tuple_remove_reported)
            for report in report_list:
                query_decrement_like = """UPDATE profile SET reported = (reported - %s)  WHERE UUID = %s"""
                tuple_decrement_like = (1, report[0])
                cursor.execute(query_decrement_like, tuple_decrement_like)

            cursor.execute(query_get_post, tuple_get_post)
            post = cursor.fetchall()

            for i in post:
                query_decrement_replies = """UPDATE post SET postReplies = (postReplies - %s) WHERE PostID = %s"""
                tuple_decrement_replies = (1, i[0])
                cursor.execute(query_decrement_replies, tuple_decrement_replies)

            query_decrement_commented = """UPDATE profile SET commented = (commented - %s) WHERE UUID = %s"""
            tuple_decrement_commented = (1, userid)
            cursor.execute(query_decrement_commented, tuple_decrement_commented)

            query_delete_reply = """UPDATE reply SET replyStatus = %s WHERE ReplyID = %s"""
            tuple_delete_reply = (0, replyid)
            cursor.execute(query_delete_reply, tuple_delete_reply)

            conn.commit()
            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def update_post(self, post_id, title, content):
        query = """UPDATE post SET postTitle = %s, postContent = %s WHERE PostID = %s AND postStatus = %s"""
        tuple = (title, content, post_id, 1)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            conn.commit()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_exist_post_by_id(self, post_id):
        query = """SELECT EXISTS(SELECT * FROM post WHERE PostID = %s AND postStatus = %s)"""
        tuple = (post_id, 1)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def select_exist_reportuser(self, postid, userid):
        query = """SELECT EXISTS(SELECT * FROM post_blacklist WHERE PostID = %s AND UUID = %s)"""
        tuple = (postid, userid)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def insert_reportedpost(self, postid, userid):
        query = """INSERT INTO post_blacklist (PostID, UUID) VALUES (%s, %s)"""
        tuple = (postid, userid)

        query_update = """UPDATE profile SET reported = (reported + %s) WHERE UUID = %s"""
        tuple_update = (1, userid)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            cursor.execute(query_update, tuple_update)
            conn.commit()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_like_by_id(self, id):
        query = """SELECT PostID, UUID FROM post_favourite WHERE PostID = %s"""
        tuple = (id,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def update_post_like_increment(self, id, userid):
        query_insert_fav = """INSERT INTO post_favourite (PostID, UUID) VALUES (%s, %s)"""
        tuple_insert_fav = (id, userid)

        query_update_profile = """UPDATE profile SET upvoted = (upvoted + %s)  WHERE UUID = %s"""
        tuple_update_profile = (1, userid)

        query_update_post = """UPDATE post SET postLikes = (postLikes + %s) WHERE PostID = %s"""
        tuple_update_post = (1, id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_insert_fav, tuple_insert_fav)
            cursor.execute(query_update_post, tuple_update_post)
            cursor.execute(query_update_profile, tuple_update_profile)

            conn.commit()
            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def update_post_like_decrement(self, id, userid):
        query_delete_fav = """DELETE FROM post_favourite WHERE PostID = %s AND UUID = %s"""
        tuple_delete_fav = (id, userid)

        query_update_profile = """UPDATE profile SET upvoted = (upvoted - %s)  WHERE UUID = %s"""
        tuple_update_profile = (1, userid)

        query_update_post = """UPDATE post SET postLikes = (postLikes - %s) WHERE PostID = %s"""
        tuple_update_post = (1, id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_delete_fav, tuple_delete_fav)
            cursor.execute(query_update_post, tuple_update_post)
            cursor.execute(query_update_profile, tuple_update_profile)

            conn.commit()
            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_saved_by_id(self, postid):
        query = """SELECT PostID, UUID FROM user_stash WHERE PostID = %s"""
        tuple = (postid,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def update_post_save_increment(self, id, userid):
        query_insert_save = """INSERT INTO user_stash (PostID, UUID) VALUES (%s, %s)"""
        tuple_insert_save = (id, userid)

        query_update_profile = """UPDATE profile SET saved = (saved + %s)  WHERE UUID = %s"""
        tuple_update_profile = (1, userid)

        query_update_post = """UPDATE post SET postSaves = (postSaves + %s) WHERE PostID = %s"""
        tuple_update_post = (1, id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_insert_save, tuple_insert_save)
            cursor.execute(query_update_post, tuple_update_post)
            cursor.execute(query_update_profile, tuple_update_profile)

            conn.commit()
            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def update_post_save_decrement(self, id, userid):
        query_delete_save = """DELETE FROM user_stash WHERE PostID = %s AND UUID = %s"""
        tuple_delete_save = (id, userid)

        query_update_profile = """UPDATE profile SET saved = (saved - %s)  WHERE UUID = %s"""
        tuple_update_profile = (1, userid)

        query_update_post = """UPDATE post SET postSaves = (postSaves - %s) WHERE PostID = %s"""
        tuple_update_post = (1, id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_delete_save, tuple_delete_save)
            cursor.execute(query_update_post, tuple_update_post)
            cursor.execute(query_update_profile, tuple_update_profile)

            conn.commit()
            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_exist_post_is_mine(self, postid, userid):
        query = """SELECT EXISTS(SELECT * FROM post WHERE PostID = %s AND UUID = %s AND postStatus = %s)"""
        tuple = (postid, userid, 1)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def delete_post_by_id(self, postid, userid):
        query_like_list = """SELECT UUID FROM post_favourite WHERE PostID = %s"""
        tuple_like_list = (postid,)

        query_save_list = """SELECT UUID FROM user_stash WHERE PostID = %s"""
        tuple_save_list = (postid,)

        query_report_list = """SELECT UUID FROM post_blacklist WHERE PostID = %s"""
        tuple_report_list = (postid,)

        query_reply_list = """SELECT ReplyID, UUID FROM reply WHERE PostID = %s"""
        tuple_reply_list = (postid,)

        query_remove_like = """DELETE FROM post_favourite WHERE PostID = %s"""
        tuple_remove_like = (postid,)

        query_remove_save = """DELETE FROM user_stash WHERE PostID = %s"""
        tuple_remove_save = (postid,)

        query_remove_reported = """DELETE FROM post_blacklist WHERE PostID = %s"""
        tuple_remove_reported = (postid,)

        query_remove_post = """UPDATE post SET postStatus = %s WHERE PostID = %s"""
        tuple_remove_post = (0, postid)

        query_decrement_posted = """UPDATE profile SET posted  = (posted - %s) WHERE UUID = %s"""
        tuple_decrement_posted = (1, userid)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_like_list, tuple_like_list)
            like_list = cursor.fetchall()

            cursor.execute(query_remove_like, tuple_remove_like)
            for like in like_list:
                query_decrement_like = """UPDATE profile SET upvoted = (upvoted - %s)  WHERE UUID = %s"""
                tuple_decrement_like = (1, like[0])
                cursor.execute(query_decrement_like, tuple_decrement_like)

            cursor.execute(query_save_list, tuple_save_list)
            save_list = cursor.fetchall()

            cursor.execute(query_remove_save, tuple_remove_save)
            for save in save_list:
                query_decrement_save = """UPDATE profile SET saved = (saved - %s)  WHERE UUID = %s"""
                tuple_decrement_save = (1, save[0])
                cursor.execute(query_decrement_save, tuple_decrement_save)

            cursor.execute(query_report_list, tuple_report_list)
            report_list = cursor.fetchall()

            cursor.execute(query_remove_reported, tuple_remove_reported)
            for report in report_list:
                query_decrement_report = """UPDATE profile SET reported = (reported - %s)  WHERE UUID = %s"""
                tuple_decrement_report = (1, report[0])
                cursor.execute(query_decrement_report, tuple_decrement_report)

            cursor.execute(query_reply_list, tuple_reply_list)
            reply_list = cursor.fetchall()

            for reply in reply_list:
                query_reply_like_list = """SELECT UUID FROM reply_favourite WHERE ReplyID = %s"""
                tuple_reply_like_list = (reply[0],)
                cursor.execute(query_reply_like_list, tuple_reply_like_list)
                reply_like_list = cursor.fetchall()

                for reply_like in reply_like_list:
                    query_decrement_reply_like = """UPDATE profile SET upvoted = (upvoted - %s)  WHERE UUID = %s"""
                    tuple_decrement_reply_like = (1, reply_like[0])
                    cursor.execute(query_decrement_reply_like, tuple_decrement_reply_like)

                query_remove_commented = """UPDATE profile SET commented = (commented - %s) WHERE UUID = %s"""
                tuple_remove_commented = (1, reply[1])
                cursor.execute(query_remove_commented, tuple_remove_commented)

                query_remove_reply = """UPDATE reply SET replyStatus = %s WHERE ReplyID = %s"""
                tuple_remove_reply = (0, reply[0])
                cursor.execute(query_remove_reply, tuple_remove_reply)

            cursor.execute(query_remove_post, tuple_remove_post)
            cursor.execute(query_decrement_posted, tuple_decrement_posted)

            conn.commit()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True
