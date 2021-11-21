from datetime import timedelta


class Config(object):
    DEBUG = True
    SECRET_KEY = "This is definitely my app secret key"


class SQL_CONFIG(Config):
    pass


class TEST_CONFIG(Config):
    # Testing setup
    TESTING = True
    SECRET_KEY = "SECRET KEY FOR TESTING ONLY"
    WTF_CSRF_ENABLED = False

    # SQL for testing only
    MYSQL_DATABASE_HOST = "127.0.0.1"
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_USER = "ssdtest"
    MYSQL_DATABASE_PASSWORD = "password1."
    MYSQL_DATABASE_DB = "test_ssd"

    # Key for testing only
    RECAPTCHA_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    RECAPTCHA_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"