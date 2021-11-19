# Importing shared resources (Inheritances)
from Bluedit.api import mysql
from Bluedit.log import error_logger


class AccountGateway:
    def select_id_name_role_by_id(self, id):
        query = """SELECT U.UUID, P.username, U.userRole FROM user U INNER JOIN profile P ON U.UUID = P.UUID WHERE U.UUID = %s"""
        tuple = (id,)

        try:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute(query, tuple)
            data = cur.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def select_account_by_email(self, email):
        query_test = """SELECT * FROM user WHERE email = %s"""
        tuple = (email,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_test, tuple)
            data = cursor.fetchone()

            conn.close()
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
        return data

    def select_otpkey_by_email(self, email):
        query = """SELECT otpkey FROM user WHERE email = %s"""
        tuple = (email,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def select_act_status_by_email(self, email):
        query = """SELECT activated FROM user WHERE email = %s"""
        tuple = (email,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def update_act_status_by_email(self, email):
        activate_value = 1
        query = """UPDATE user SET activated = %s WHERE email = %s"""
        tuple = (activate_value, email)

        query_get_id = """SELECT UUID FROM user WHERE email = %s"""
        tuple_get_id = (email,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            conn.commit()

            cursor.execute(query_get_id, tuple_get_id)
            data = cursor.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def select_exist_email(self, email):
        query = """SELECT EXISTS(SELECT * FROM user WHERE email = %s)"""
        tuple = (email,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def select_userid_by_email(self, email):
        query = """SELECT UUID FROM user WHERE email =  %s"""
        tuple = (email,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def select_exist_salt(self, salt):
        query = """SELECT EXISTS(SELECT * FROM user WHERE salt = %s)"""
        tuple = (salt,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def update_password_by_email(self, email, pw, salt, time):
        query = """UPDATE user SET password = %s, salt = %s, passwordDate = %s WHERE email = %s"""
        tuple = (pw, salt, time, email)

        query_get_id = """SELECT UUID FROM user WHERE email = %s"""
        tuple_get_id = (email,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            conn.commit()

            cursor.execute(query_get_id, tuple_get_id)
            data = cursor.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def select_exist_username(self, username):
        query = """SELECT EXISTS(SELECT * FROM profile WHERE username =  %s)"""
        tuple = (username,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            print(data)

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def select_exist_otpkey(self, otpkey):
        query = """SELECT EXISTS(SELECT * FROM user WHERE otpkey =  %s)"""
        tuple = (otpkey,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def insert_new_user(self, account, uname):
        default_role = "user"
        default_about = "Hello there, I am new to Bluedit."
        default_img = "../../static/profile_image/default/default_profile.png"
        default_num = 0

        query_user ="""INSERT INTO user VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        tuple_user = (account.userID, account.email, account.password, account.salt, account.accStatus, account.dateCreated, default_role, account.activated, account.emailAuth, account.otpkey, account.passwordDate)

        query_profile = """INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        tuple_profile = (account.userID, uname, default_about, default_num, default_num, default_num, default_num, default_num, default_img)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query_user, tuple_user)
            cursor.execute(query_profile, tuple_profile)

            conn.commit()

            conn.close()
            return True
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def select_authenticate_email(self, id, email):
        query = """SELECT EXISTS(SELECT email FROM user WHERE email = %s AND UUID = %s)"""
        tuple = (email, id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def update_email_by_id(self, email, id, time):
        auth = 1
        activated = 0
        query = """UPDATE user SET email = %s, dateCreated = %s, activated = %s, emailAuth = %s WHERE UUID = %s"""
        tuple = (email, time, activated, auth, id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            conn.commit()

            conn.close()
            return True
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def select_passwordsalt_by_id(self, id):
        query = """SELECT password, salt FROM user WHERE UUID = %s"""
        tuple = (id,)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            data = cursor.fetchone()

            conn.close()
            return data
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def update_password_by_id(self, id, pw, salt, time):
        query = """UPDATE user SET password = %s, salt = %s, passwordDate = %s WHERE UUID = %s"""
        tuple = (pw, salt, time, id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            conn.commit()

            conn.close()
            return True
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)

    def update_tfa_by_id(self, id, tfa):
        query = """UPDATE user SET emailAuth = %s WHERE UUID = %s"""
        tuple = (int(tfa), id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(query, tuple)
            conn.commit()

            conn.close()
            return True
        except Exception as e:
            error_logger.error("Encountered error while accessing the database - " + str(e))
            return str(e)
