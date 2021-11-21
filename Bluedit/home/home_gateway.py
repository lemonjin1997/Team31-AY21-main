# Importing shared resources (Inheritances)
from Bluedit.api import mysql
from Bluedit.log import error_logger


class HomeGateway:
    def get_all_post(self):
        query_post = """SELECT * FROM post INNER JOIN profile ON post.UUID = profile.UUID WHERE postStatus = %s ORDER BY postTime DESC"""
        tuple_post = (1,)

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

    def get_all_post_with_conditions(self, target, value):
        query_post = """SELECT * FROM post INNER JOIN profile ON post.UUID = profile.UUID WHERE postStatus = %s AND """ + target + """ LIKE %s ORDER BY postTime DESC"""    #nosec
        tuple_post = (1, "%"+value+"%")

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

    def select_like_by_userid(self, userid):
        query = """SELECT PostID, UUID FROM post_favourite WHERE UUID = %s"""
        tuple = (userid,)

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

    def select_save_by_userid(self, userid):
        query = """SELECT PostID, UUID FROM user_stash WHERE UUID = %s"""
        tuple = (userid,)

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

    def select_r_like_by_userid(self, userid):
        query = """SELECT ReplyID, UUID FROM reply_favourite WHERE UUID = %s"""
        tuple = (userid,)

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
