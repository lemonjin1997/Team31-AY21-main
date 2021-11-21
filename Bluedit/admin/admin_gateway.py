# Importing shared resources (Inheritances)
from Bluedit.api import mysql
from Bluedit.log import error_logger


class AdminGateway:
    def select_all_user(self):
        value = 1
        role = "user"

        query = """SELECT user.dateCreated, user.UUID, profile.username, user.userRole FROM profile INNER JOIN user ON profile.UUID = user.UUID WHERE user.activated = %s AND user.accStatus = %s AND userRole = %s"""
        tuple = (value, value, role)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def update_userrole_by_id(self, userid):
        role = "admin"
        query = """UPDATE user SET userRole = %s WHERE UUID = %s"""
        tuple = (role, userid)

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

    def select_reported_post_list(self):
        query = """SELECT post.PostID, postTitle, postContent, COUNT(*) FROM post_blacklist INNER JOIN post ON post.PostID = post_blacklist.PostID GROUP BY PostID"""
        tuple = ()

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def select_locked_post(self):
        query = """SELECT PostID FROM post WHERE postLock = %s AND postStatus = %s"""
        tuple = (1, 1)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def select_lockstatus_by_id(self, postid):
        query = """SELECT postLock FROM post WHERE PostID = %s"""
        tuple = (postid,)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def update_postlock(self, postid):
        query = """UPDATE post SET postLock = %s WHERE PostID = %s"""
        tuple = (1, postid)

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

    def update_postlock_unlock(self, postid):
        query = """UPDATE post SET postLock = %s WHERE PostID = %s"""
        tuple = (0, postid)

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

    def select_reported_reply_list(self):
        query = """SELECT reply.ReplyID, replyContent, COUNT(*) FROM reply_blacklist INNER JOIN reply ON reply.ReplyID = reply_blacklist.ReplyID GROUP BY ReplyID"""
        tuple = ()

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def select_all_user_by_auth(self):
        value = 1
        role = "user"
        query = """SELECT user.dateCreated, user.UUID, profile.username, user.userRole FROM profile INNER JOIN user ON profile.UUID = user.UUID WHERE user.activated = %s AND userRole = %s"""
        tuple = (value, role)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def select_banned_userid(self):
        role = 'user'
        query = """SELECT UUID FROM user WHERE activated = %s AND userRole = %s AND accStatus = %s"""
        tuple = (1, role, 0)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def select_banstatus_by_id(self, userid):
        query = """SELECT accStatus FROM user WHERE UUID = %s"""
        tuple = (userid,)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchall()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def update_user_accStatus(self, userid):
        query = """UPDATE user SET accStatus = %s WHERE UUID = %s"""
        tuple = (0, userid)

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

    def update_user_accStatus_unban(self, userid):
        query = """UPDATE user SET accStatus = %s WHERE UUID = %s"""
        tuple = (1, userid)

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
