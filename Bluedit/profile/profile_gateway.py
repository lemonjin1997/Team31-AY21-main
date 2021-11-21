# Importing shared resources (Inheritances)
from Bluedit.api import mysql
from Bluedit.log import error_logger


class ProfileGateway:
    def select_exist_name(self, name):
        query = """SELECT EXISTS(SELECT username FROM profile WHERE username = %s)"""
        tuple = (name,)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchone()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def select_profile_by_name(self, name):
        query = """SELECT * FROM profile WHERE username = %s"""
        tuple = (name,)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchone()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def select_top3user_post_by_name(self, name):
        query_post = """SELECT * FROM post INNER JOIN profile ON post.UUID = profile.UUID WHERE profile.username = %s AND post.postStatus = %s ORDER BY postTime DESC LIMIT 3"""
        tuple = (name, 1)

        query_category = """SELECT CatName, PostID FROM post_category"""
        tuple_cat = ()

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_post, tuple)
            post = cursor.fetchall()

            cursor.execute(query_category, tuple_cat)
            category = cursor.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return [post, category]

    def update_image_by_nameid(self, path, name, id):
        query = """UPDATE profile SET profile_img = %s WHERE username = %s AND UUID = %s"""
        tuple = (path, name, id)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            conn.commit()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_fa_by_id(self, id):
        query = """SELECT emailAuth FROM user WHERE UUID = %s"""
        tuple = (id,)

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

    def update_name_by_nameid(self, cur_name, input_name, id):
        query = """UPDATE profile SET username = %s WHERE username = %s AND UUID = %s"""
        tuple = (input_name, cur_name, id)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            conn.commit()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def update_about_by_nameid(self, name, id, about):
        query = """UPDATE profile SET about = %s WHERE username = %s AND UUID = %s"""
        tuple = (about, name, id)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            conn.commit()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return True

    def select_user_post_by_name(self, name):
        query_post = """SELECT * FROM post INNER JOIN profile ON post.UUID = profile.UUID WHERE profile.username = %s AND post.postStatus = %s ORDER BY postTime DESC"""
        tuple_post = (name, 1)

        query_category = """SELECT CatName, PostID FROM post_category"""
        tuple_cat = ()

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

    def select_stashed_post_by_id(self, id):
        query_post = """SELECT * FROM user_stash U INNER JOIN post P ON U.PostID = P.PostID INNER JOIN profile PF ON P.UUID = PF.UUID WHERE U.UUID = %s AND P.postStatus = %s ORDER BY postTime DESC"""
        tuple_post = (id, 1)

        query_category = """SELECT CatName, PostID FROM post_category"""
        tuple_cat = ()

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

    def select_upvote_post_by_id(self, id):
        query_post = """SELECT * FROM post_favourite U INNER JOIN post P ON U.PostID = P.PostID INNER JOIN profile PF ON P.UUID = PF.UUID WHERE U.UUID = %s AND P.postStatus = %s ORDER BY postTime DESC"""
        tuple_post = (id, 1)

        query_category = """SELECT CatName, PostID FROM post_category"""
        tuple_cat = ()

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

    def select_upvoted_reply_by_id(self, id):
        query = """SELECT * FROM reply_favourite RF INNER JOIN reply R ON RF.ReplyID = R.ReplyID INNER JOIN post PT ON R.PostID = PT.PostID INNER JOIN profile P ON R.UUID = P.UUID WHERE RF.UUID = %s AND R.replyStatus = %s"""
        tuple = (id, 1)

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

    def select_commented_post_by_id(self, id):
        query = """SELECT * FROM reply INNER JOIN post ON post.PostID = reply.PostID INNER JOIN profile ON post.UUID = profile.UUID WHERE reply.UUID = %s AND replyStatus = %s ORDER BY replyTime DESC"""
        tuple = (id, 1)

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
