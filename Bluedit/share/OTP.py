import pyotp


class OTP(object):
    def create_otp_generator(self, key):
        return pyotp.TOTP(key, interval=120)
