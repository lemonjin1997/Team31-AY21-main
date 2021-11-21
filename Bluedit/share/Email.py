from Bluedit.api import mail
from itsdangerous import URLSafeTimedSerializer
from config import Config
from flask_mail import Message


class Email(object):
    # Generate a reversible encrypted email string to act as the url parameter
    def generate_token(self, email):
        key = URLSafeTimedSerializer(Config.SECRET_KEY)
        return key.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)

    # Decrypt the token generated to return the user email for verification
    # 3600s = 1 hour (url remain valid for an hour upon creation)
    def decrypt_token(self, token, expiration=3600):
        key = URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            email = key.loads(
                token,
                salt=Config.SECURITY_PASSWORD_SALT,
                max_age=expiration
            )
        except:
            return False

        return email
