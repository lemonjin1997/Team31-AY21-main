# Importing Account table gateway
import hashlib
import string
import random

import pyotp

from Bluedit.auth.auth_gateway import AccountGateway
from Bluedit.auth.models.Account import Account
from Bluedit.share.OTP import OTP
from Bluedit.share.Sanitizer import Sanitizer
from Bluedit.share.Generator import Generator
from Bluedit.share.Email import Email
from Bluedit.api import mail
from config import Config
from flask_mail import Message


class AccountManager(OTP, Sanitizer, Email, Generator):
    def __init__(self):
        self.gateway = AccountGateway()

    def load_user(self, id):
        if id is None: return None

        data = self.gateway.select_id_name_role_by_id(id)
        if isinstance(data, str):
            return -1
        else:
            return data

    def get_account_by_email(self, email):
        data = self.gateway.select_account_by_email(email)

        if isinstance(data, str):
            return -1
        elif not data:
            return None
        else:
            account = Account(data[0], data[1], data[2], data[3], data[5], data[4], data[7], data[8], data[9], data[10])
            return account

    # Using salt and password to generate a sha256 hash value
    def hash(self, password, salt):
        return hashlib.sha256(str(password + salt).encode()).hexdigest()

    def get_otp_key(self, email):
        data = self.gateway.select_otpkey_by_email(email)

        if isinstance(data, str):
            return -1
        elif not data:
            return False
        else:
            return data[0]

    def send_email(self, to, subject, template):
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=Config.MAIL_DEFAULT_SENDER
        )
        mail.send(msg)

    def check_activation(self, email):
        data = self.gateway.select_act_status_by_email(email)

        if isinstance(data, str):
            return -1
        elif not data:
            return -2
        else:
            return data[0]

    def activate_account(self, email):
        result = self.gateway.update_act_status_by_email(email)

        if isinstance(result, str):
            return -1
        else:
            return result

    def email_exist(self, email):
        result = self.gateway.select_exist_email(email)

        if isinstance(result, str):
            return -1
        elif result[0] == 1:
            return True
        else:
            return False

    def get_userid(self, email):
        data = self.gateway.select_userid_by_email(email)

        if isinstance(data, str):
            return -1
        elif not data:
            return False
        else:
            return data[0]

    def generate_salt(self):
        unique = False
        salt = ""

        while not unique:
            salt = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in
                range(16))
            result = self.gateway.select_exist_salt(salt)

            if result[0] == 0:
                unique = True
            elif result[0] == 1:
                continue
            else:
                return -1
        return salt

    def update_password(self, email, pw, salt):
        result = self.gateway.update_password_by_email(email, pw, salt, self.generate_time())

        if isinstance(result, str):
            return -1
        else:
            return result[0]

    def username_exist(self, username):
        result = self.gateway.select_exist_username(username)

        if isinstance(result, str):
            return -1
        elif result[0] == 1:
            return True
        else:
            return False

    def generate_otpkey(self):
        unique = False
        key = ""

        while not unique:
            key = pyotp.random_base32()
            result = self.gateway.select_exist_otpkey(key)

            if result[0] == 0:
                unique = True
            elif result[0] == 1:
                continue
            else:
                return -1
        return key

    def create_account(self, salt, otpkey, email, pw, uname):
        id = self.generate_id()
        time = self.generate_time()
        account = Account(id, email, pw, salt, time, 1, 0, 1, otpkey, time)

        result = self.gateway.insert_new_user(account, uname)

        if isinstance(result, str):
            return -1
        else:
            return id

    def authenticate_email(self, id, email):
        data = self.gateway.select_authenticate_email(id, email)

        if isinstance(data, str):
            return -1
        elif data[0] == 1:
            return True
        else:
            return False

    def update_email(self, email, id):
        result = self.gateway.update_email_by_id(email, id, self.generate_time())

        if isinstance(result, str):
            return -1
        else:
            return result

    def get_password(self, id):
        data = self.gateway.select_passwordsalt_by_id(id)

        if isinstance(data, str):
            return -1
        else:
            return data

    def update_password_by_id(self, id, pw, salt):
        result = self.gateway.update_password_by_id(id, pw, salt, self.generate_time())

        if isinstance(result, str):
            return -1
        else:
            return result

    def update_tfa(self, id, tfa):
        result = self.gateway.update_tfa_by_id(id, tfa)

        if isinstance(result, str):
            return -1
        else:
            return result
