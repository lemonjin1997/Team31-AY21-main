import unittest
import datetime
from unittest import mock

from Bluedit import create_app
from config import TEST_CONFIG
from flask_testing import TestCase
from Bluedit.api import login_manager


class Functional_Test(TestCase):
    def create_app(self):
        conf = TEST_CONFIG
        app = create_app(conf)
        app.config.update({
            'LOGIN_DISABLED': True
        })
        login_manager.init_app(app)
        return app

    def test_GET_loginPage(self):
        rv = self.client.get("/auth/login", follow_redirects=True)
        assert b'"login_form" method="POST" action="/auth/login">' in rv.data
        self.assertStatus(rv, 200)
        self.assert_template_used("login.html")

    def test_GET_registerPage(self):
        rv = self.client.get("/auth/register", follow_redirects=True)
        assert b'<title>Bluedit - Register</title>' in rv.data
        self.assertStatus(rv, 200)
        self.assert_template_used("register.html")

    def test_GET_verifyaccountPage(self):
        rv = self.client.get("/auth/verify_account", follow_redirects=True)
        assert b'<title>Bluedit - Account Verification</title>' in rv.data
        self.assertStatus(rv, 200)
        self.assert_template_used("account_verify.html")

    def test_GET_verifyaccounttokenPage(self):
        rv = self.client.get(
            "/auth/verify_account/verify/InJ5YW5senIxOTk3QGdtYWlsLmNvbSI.YYgt4Q.mHs2UfQ8u5yMioAJa3C1_-PWNR4",
            follow_redirects=True)

        # Using an invalid token thus this msg exist
        assert b'Verification error. Token have expired' in rv.data
        self.assertStatus(rv, 200)
        self.assert_template_used("account_verify_token.html")

    def test_GET_loginotpverificationPage_withsession(self):
        with self.client.session_transaction() as session:
            session["otp_credentials"] = ["test@gmail.com", "some_user_id"]

        rv = self.client.get("/auth/login/otp_verification", follow_redirects=True)
        assert b'<p>Please enter the otp' in rv.data
        self.assertStatus(rv, 200)
        self.assert_template_used("login_otp.html")

    def test_GET_loginotpverificationPage_withoutsession(self):
        rv = self.client.get("/auth/login/otp_verification", follow_redirects=True)
        assert b'"login_form" method="POST" action="/auth/login">' in rv.data
        self.assertStatus(rv, 200)
        self.assert_template_used("login.html")

    def test_GET_forgetpasswordPage(self):
        rv = self.client.get("/auth/forget_password", follow_redirects=True)
        assert b'A link will only be generated and sent if the' in rv.data
        self.assertStatus(rv, 200)
        self.assert_template_used("forget_password.html")

    def test_GET_forgetpasswordtokenPage(self):
        rv = self.client.get("/auth/forget_password/InJ5YW5senIxOTk3QGdtYWlsLmNvbSI.YXpuLA.UfnuOUIc3ixqF9DULHIYg3A9Mpg",
                             follow_redirects=True)

        assert b'<title>Bluedit - Forget Password</title' in rv.data
        self.assertStatus(rv, 200)
        self.assert_template_used("forget_password_token.html")


    def test_GET_profilePage(self):
        rv = self.client.get("/profile/user/t@st", follow_redirects=True)

        assert b'<p> - "t@st" does not exist, are you sure you have searched for the correct person ?</p>' in rv.data
        self.assertStatus(rv, 200)
        self.assert_template_used("profile.html")



if __name__ == "__main__":
    unittest.main()