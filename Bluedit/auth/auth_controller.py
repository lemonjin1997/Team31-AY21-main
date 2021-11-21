# Importing open-source API(s)
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, login_user, logout_user, current_user

# Importing required dependencies (Within own domain)
from werkzeug.exceptions import abort

from Bluedit.auth.models.AccountManager import AccountManager
from Bluedit.auth.models.User import User

# Importing required dependencies (From shared)
from Bluedit.api import recaptcha, login_manager
from Bluedit.log import auth_logger_info

auth_bp = Blueprint('auth_bp', __name__, template_folder="templates")
auth_manager = AccountManager()


@auth_bp.route('/auth/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        status = ["none", None, "alert-danger"] if session.get("login_auth_status") is None else session.get(
            "login_auth_status")
        session.pop("login_auth_status", None)
        session.pop("verify_email", None)
        session.pop("otp_credentials", None)

        return render_template("login.html", status=status)
    elif request.method == "POST":
        # 1) Declaring variables
        email, password = request.form["email"], request.form["password"]
        fail_msg = "Authentication Failed. Please check that you have entered the correct email or password"
        ban_msg = "Login Failed. This account have been banned by the administrators"
        captcha_msg = "Authentication Failed. ReCatpcha validation failed"

        if not recaptcha.verify():
            session["login_auth_status"] = ["null", captcha_msg, "alert-danger"]
            return redirect(url_for('auth_bp.login'))

        # 2) Validating inputs
        if not auth_manager.validate_email_MatchFormat(email) or not auth_manager.validate_password_MatchFormat(
                password):
            session["login_auth_status"] = ["null", fail_msg, "alert-danger"]
            return redirect(url_for('auth_bp.login'))

        # 2) Get account details
        account = auth_manager.get_account_by_email(email)
        if account == -1:
            abort(500)
        elif not account:
            session["login_auth_status"] = ["null", fail_msg, "alert-danger"]
            return redirect(url_for('auth_bp.login'))

        # 3) Hash the input password
        pw_hash = auth_manager.hash(password, account.salt)

        # 4) Compare the hashes
        if pw_hash != account.password:
            # Log authentication (Failed Login)
            auth_logger_info.warning("There is a failed attempt to access the application via user " + account.userID)

            session["login_auth_status"] = ["null", fail_msg, "alert-danger"]
            return redirect(url_for('auth_bp.login'))

        # 5) Check account if it have been banned
        if account.accStatus != 1:
            session["login_auth_status"] = ["null", ban_msg, "alert-danger"]
            return redirect(url_for('auth_bp.login'))

        # 6) Check account if it have been verified
        if account.activated != 1:
            session["verify_email"] = account.email
            return redirect(url_for("auth_bp.verify_account"))

        # 7) Check account if it have otp enabled
        if account.emailAuth == 1:
            session["otp_credentials"] = [account.email, account.userID]

            token = auth_manager.create_otp_generator(account.otpkey).now()
            html = render_template('email_template/otp_email.html', otp=token)
            subject = "Bluedit login verification: " + token
            auth_manager.send_email(email, subject, html)

            # Log authentication (OTP Email)
            auth_logger_info.info("OTP token email have been sent to the email registered under user " + account.userID)

            return redirect(url_for('auth_bp.login_otp_verification'))

        # 8) Login user
        u = load_user(account.userID)
        if u is None:
            session["login_auth_status"] = ["null", fail_msg, "alert-danger"]
            return redirect(url_for('auth_bp.login'))

        login_user(u)

        # Log authentication (Login)
        auth_logger_info.info("User " + account.userID + " logged in to the application")

        return redirect(url_for('home_bp.home'))
    else:
        abort(404)


@auth_bp.route('/auth/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        status = ["none", None, "alert-danger"] if session.get("register_auth_status") is None else session.get(
            "register_auth_status")
        session.pop("register_auth_status", None)
        session.pop("verify_email", None)
        session.pop("otp_credentials", None)

        return render_template("register.html", status=status)
    elif request.method == "POST":
        # 1) Declare Variables
        uname, email, pw, cfm_pw = request.form["username"], request.form["email"], request.form["password"], \
                                   request.form["cfm_password"]
        fail_msg = "Validation error. Please verify that all your inputs matches the requirements"
        captcha_msg = "Validation error. Recaptcha is not checked or is invalid"
        name_exist_msg = "Validation error. This username have already been used"
        email_exist_msg = "Validation error. This email have already been used"
        both_exist_msg = "Validation error. Both the username and email have already been used"

        # 2) Check recaptcha
        if not recaptcha.verify():
            session["register_auth_status"] = ["null", captcha_msg, "alert-danger"]
            return redirect(url_for('auth_bp.register'))

        # 3) Validate all inputs
        if not auth_manager.validate_input_NoSpecialCharacters(uname) \
                or not auth_manager.validate_email_MatchFormat(email) \
                or not auth_manager.validate_password_MatchFormat(pw) \
                or not auth_manager.validate_password_MatchFormat(cfm_pw):
            session["register_auth_status"] = ["null", fail_msg, "alert-danger"]
            return redirect(url_for('auth_bp.register'))

        # 4) Check if uname and email exist
        username_exist = auth_manager.username_exist(uname)
        email_exist = auth_manager.email_exist(email)

        if username_exist and email_exist:
            session["register_auth_status"] = ["null", both_exist_msg, "alert-danger"]
            return redirect(url_for('auth_bp.register'))
        elif username_exist:
            session["register_auth_status"] = ["null", name_exist_msg, "alert-danger"]
            return redirect(url_for('auth_bp.register'))
        elif email_exist:
            session["register_auth_status"] = ["null", email_exist_msg, "alert-danger"]
            return redirect(url_for('auth_bp.register'))

        # 5) Check if password and cfm-password matches
        if pw != cfm_pw:
            session["register_auth_status"] = ["null", fail_msg, "alert-danger"]

        # 6) Generate salt and otp key
        salt = auth_manager.generate_salt()
        otpkey = auth_manager.generate_otpkey()
        if salt == -1 or otpkey == -1:
            abort(500)

        # 7) Hash the password
        hash_pw = auth_manager.hash(pw, salt)

        # 7) Create the account
        create_account = auth_manager.create_account(salt, otpkey, email, hash_pw, uname)
        if create_account == -1: abort(500)

        # Log authentication
        auth_logger_info.info("User " + create_account + " just registered to the application under username " + uname)

        session["verify_email"] = email
        return redirect(url_for("auth_bp.verify_account"))
    else:
        abort(404)


@auth_bp.route('/auth/verify_account', methods=["GET", "POST"])
def verify_account():
    if request.method == "GET":
        status = ["none", None, "alert-danger"] if session.get("verify_auth_status") is None else session.get(
            "verify_auth_status")
        session.pop("verify_auth_status", None)

        return render_template("account_verify.html", status=status)
    elif request.method == "POST":
        # 1) Declare Variables
        email = session.get("verify_email")
        auth_msg = "Authentication failed. Please re-login to initiate the verification process"
        captcha_msg = "Validation error. Recaptcha is not checked or is invalid"

        # 2) Check if email exist in session
        if email is None:
            session["login_auth_status"] = ["null", auth_msg, "alert-danger"]
            return redirect(url_for("auth_bp.login"))

        # 3) Check if recaptcha is valid
        if not recaptcha.verify():
            session["verify_auth_status"] = ["null", captcha_msg, "alert-danger"]
            return redirect(url_for('auth_bp.verify_account'))

        # 4) Send verification email
        email_token = auth_manager.generate_token(email)
        confirm_url = url_for('auth_bp.verify_account_token', email_token=email_token, _external=True)
        html = render_template('email_template/verification_email.html', confirm_url=confirm_url)
        subject = "Verify your Bluedit email address"
        auth_manager.send_email(email, subject, html)

        # Log authentication
        auth_logger_info.info("Verification link have been generated and sent out")

        return redirect(url_for('auth_bp.verify_account'))
    else:
        abort(404)


# -----------------------------------------------------------------------

@auth_bp.route('/auth/verify_account/verify/<email_token>', methods=["GET"])
def verify_account_token(email_token):
    if request.method == "GET":
        # 1) Remove session
        session.pop("verify_email", None)

        # 2) Defining Variables
        verify_msg = "Verification error. Token have expired or is invalid"
        auth_msg = "Authentication error. Email does not exist"
        act_msg = "Activated. Your account have already been activated. You may proceed to login"
        success_msg = "Activated. Your account is now activated. You may proceed to login"

        # 3) Check token to see if it is valid
        email = auth_manager.decrypt_token(email_token)
        if not email:
            account_token_auth_status = ["null", verify_msg, "alert-danger"]
            return render_template("account_verify_token.html", status=account_token_auth_status)

        # 4) Check account activation
        activation_status = auth_manager.check_activation(email)
        if activation_status == -1: abort(500)

        if activation_status == -2:
            account_token_auth_status = ["null", auth_msg, "alert-danger"]
        elif activation_status == 1:
            account_token_auth_status = ["null", act_msg, "alert-success"]
        else:
            activate_account = auth_manager.activate_account(email)
            if activate_account == -1: abort(500)

            # Log authentication
            auth_logger_info.info("User " + activate_account[0] + " just activated his/her account")

            account_token_auth_status = ["null", success_msg, "alert-success"]

        return render_template("account_verify_token.html", status=account_token_auth_status)
    else:
        abort(404)


@auth_bp.route('/auth/login/otp_verification', methods=["GET", "POST"])
def login_otp_verification():
    if request.method == "GET":
        credentials = session.get("otp_credentials")

        auth_msg = "Authentication failed. Please re-login to complete your 2FA authentication process"

        if credentials is None:
            session["login_auth_status"] = ["null", auth_msg, "alert-danger"]
            return redirect(url_for('auth_bp.login'))

        status = ["none", None, "alert-danger"] if session.get("otp_auth_status") is None else session.get(
            "otp_auth_status")
        session.pop("otp_auth_status", None)

        return render_template("login_otp.html", status=status)
    elif request.method == "POST":
        # 1) Declaring Variables
        credentials = session.get("otp_credentials")
        auth_msg = "Authentication failed. Please re-login to restart the otp process"
        verify_msg = "Verification failed. Token does not match"

        # 2) Form ;submit_otp; actions
        if request.form.get('submit_otp'):
            otp_input = request.form["digit-1"] + \
                        request.form["digit-2"] + \
                        request.form["digit-3"] + \
                        request.form["digit-4"] + \
                        request.form["digit-5"] + \
                        request.form["digit-6"]

            # 2a) Get user otp_key
            otpkey = auth_manager.get_otp_key(credentials[0])
            if otpkey == -1:
                abort(500)
            elif not otpkey:
                session["login_auth_status"] = ["null", auth_msg, "alert-danger"]
                session.pop("otp_credentials", None)
                return redirect(url_for('auth_bp.login'))

            # 2b) Compare otp token with input
            cur_token = auth_manager.create_otp_generator(otpkey).now()
            if str(otp_input) != str(cur_token):
                session["otp_auth_status"] = ["null", verify_msg, "alert-danger"]
                return redirect(url_for('auth_bp.login_otp_verification'))

            session.pop("otp_credentials", None)

            # 2c) Login user
            u = load_user(credentials[1])
            if u is None:
                session["login_auth_status"] = ["null", auth_msg, "alert-danger"]
                return redirect(url_for('auth_bp.login'))

            login_user(u)

            # Log authentication (Login)
            auth_logger_info.info("User " + credentials[1] + " logged in to the application after passing email OTP")

            return redirect(url_for('home_bp.home'))
        # 3) Form ;resend_otp; actions
        elif request.form.get('resend_otp'):
            # 3a) Get user otp_key
            otpkey = auth_manager.get_otp_key(credentials[0])
            if otpkey == -1:
                abort(500)
            elif not otpkey:
                session["login_auth_status"] = ["null", auth_msg, "alert-danger"]
                session.pop("otp_credentials", None)
                return redirect(url_for('auth_bp.login'))

            # 3b) Send otp email
            token = auth_manager.create_otp_generator(otpkey).now()
            html = render_template('email_template/otp_email.html', otp=token)
            subject = "Bluedit login verification: " + token
            auth_manager.send_email(credentials[0], subject, html)

            # Log authentication (OTP Email)
            auth_logger_info.info("OTP token email have been sent to the email registered under user " + credentials[1])

            return redirect(url_for('auth_bp.login_otp_verification'))
    else:
        abort(404)


@auth_bp.route('/auth/forget_password', methods=["GET", "POST"])
def forget_password():
    if request.method == "GET":
        status = ["none", None, "alert-danger"] if session.get("forget_pass_auth_status") is None else session.get(
            "forget_pass_auth_status")
        session.pop("forget_pass_auth_status", None)

        return render_template("forget_password.html", status=status)
    elif request.method == "POST":
        # 1) Declaring variables
        email = request.form["email"]
        auth_msg = "Validation error. Please verify that all your inputs matches the requirements"
        captcha_msg = "Validation error. Recaptcha is not checked or is invalid"
        send_msg = "Validation successful. If email exist, an email will be sent to it"

        # 2) Validate Recaptcha
        if not recaptcha.verify():
            session["forget_pass_auth_status"] = ["null", captcha_msg, "alert-danger"]
            return redirect(url_for('auth_bp.forget_password'))

        # 3) Validate email input
        if not auth_manager.validate_email_MatchFormat(email):
            session["forget_pass_auth_status"] = ["null", auth_msg, "alert-danger"]
            return redirect(url_for('auth_bp.forget_password'))

        # 4) Check if email exist
        email_exist = auth_manager.email_exist(email)
        if email_exist == -1:
            abort(500)
        elif not email_exist:
            session["login_auth_status"] = ["null", send_msg, "alert-success"]
            return redirect(url_for('auth_bp.login'))

        id = auth_manager.get_userid(email)
        if id == -1:
            abort(500)
        elif not id:
            session["login_auth_status"] = ["null", send_msg, "alert-success"]
            return redirect(url_for('auth_bp.login'))

        # 5) Send reset link
        reset_token = auth_manager.generate_token(email)
        reset_url = url_for('auth_bp.forget_password_token', reset_token=reset_token, _external=True)
        html = render_template('email_template/forget_password_email.html', reset_url=reset_url)
        subject = "Reset Password Instructions"
        auth_manager.send_email(email, subject, html)

        # Log authentication
        auth_logger_info.info("User " + id + " requested for a password change")
        auth_logger_info.info("Forget password link have been sent to user " + id)

        session["login_auth_status"] = ["null", send_msg, "alert-success"]
        return redirect(url_for('auth_bp.login'))
    else:
        abort(404)


# -----------------------------------------------------------------------

@auth_bp.route('/auth/forget_password/<reset_token>', methods=["GET", "POST"])
def forget_password_token(reset_token):
    if request.method == "GET":
        status = ["none", None, "alert-danger"] if session.get("reset_auth_status") is None else session.get(
            "reset_auth_status")
        session.pop("reset_auth_status", None)

        return render_template("forget_password_token.html", status=status, reset_token=reset_token)
    elif request.method == "POST":
        # 1) Declaring variables
        input_email, pw, cfm_pw = request.form["email"], request.form["password"], request.form["cfm_password"]
        verify_msg = "Verification error. Token have expired or is invalid"
        catpcha_msg = "Validation error. Recaptcha is not checked or is invalid"
        fail_msg = "Validation error. Please verify that all your inputs matches the requirements"
        err_msg = "Authentication error. Email does not match the token"
        success_msg = "Updated. Password have been updated"

        # 2) Verify token
        email = auth_manager.decrypt_token(reset_token)
        if not email:
            session["login_auth_status"] = ["null", verify_msg, "alert-danger"]
            return redirect(url_for("auth_bp.login"))

        # 3) Recaptcha verification
        if not recaptcha.verify():
            session["reset_auth_status"] = ["null", catpcha_msg, "alert-danger"]
            return redirect(url_for('auth_bp.forget_password_token', reset_token=reset_token))

        # 4) Verify input
        if not auth_manager.validate_email_MatchFormat(input_email) or \
                not auth_manager.validate_password_MatchFormat(pw) or \
                not auth_manager.validate_password_MatchFormat(cfm_pw):
            session["reset_auth_status"] = ["null", fail_msg, "alert-danger"]
            return redirect(url_for('auth_bp.forget_password_token', reset_token=reset_token))

        # 5) Validate email matches
        if input_email != email:
            session["reset_auth_status"] = ["null", err_msg, "alert-danger"]
            return redirect(url_for('auth_bp.forget_password_token', reset_token=reset_token))

        # 6) Generate new salt
        salt = auth_manager.generate_salt()
        if salt == -1: abort(500)

        # 7) Hash the new pw
        hash_pw = auth_manager.hash(pw, salt)

        # 8) Update password
        update_password = auth_manager.update_password(email, hash_pw, salt)
        if update_password == -1: abort(500)

        # Log authentication
        auth_logger_info.info("User " + update_password + " successfully changed his/her password")

        session["login_auth_status"] = ["null", success_msg, "alert-success"]
        return redirect(url_for("auth_bp.login"))
    else:
        abort(404)


@auth_bp.route('/auth/management/update_email', methods=["POST"])
@login_required
def manage_profile_update_email():
    if request.method == "POST":
        # 1) Declaring Variables
        cur_email, new_email = request.form["current-email"], request.form["new-email"]
        err_msg = "Validation error. Please verify that all your inputs matches the requirements"
        auth_msg = "Authentication failed. Current email mismatch"
        exist_msg = "Update failed. New email is already in used"
        success_msg = "Update success. Email updated, please re-login to verify yourself"

        # 2) Validating the inputs
        if not auth_manager.validate_email_MatchFormat(cur_email) or not auth_manager.validate_email_MatchFormat(
                new_email):
            session["profile_manage_auth_status"] = ["null", err_msg, "alert-danger"]
            return redirect(url_for('profile_bp.manage_profile'))

        # 3) Authenticate from current email
        authenticate_email = auth_manager.authenticate_email(current_user.id, cur_email)
        if authenticate_email == -1:
            abort(500)
        elif not authenticate_email:
            session["profile_manage_auth_status"] = ["null", auth_msg, "alert-danger"]
            return redirect(url_for('profile_bp.manage_profile'))

        # 4) Check new email unique
        email_exist = auth_manager.email_exist(new_email)
        if email_exist == -1:
            abort(500)
        elif email_exist:
            session["profile_manage_auth_status"] = ["null", exist_msg, "alert-danger"]
            return redirect(url_for('profile_bp.manage_profile'))

        # 5) Update email
        update_email = auth_manager.update_email(new_email, current_user.id)
        if update_email == -1: abort(500)

        # Log authentication
        auth_logger_info.info("User " + current_user.id + " successfully changed his/her email")

        session.clear()
        logout_user()

        session["login_auth_status"] = ["null", success_msg, "alert-success"]
        return redirect(url_for('auth_bp.login'))
    else:
        abort(404)


# -----------------------------------------------------------------------
@auth_bp.route('/auth/management/update_password', methods=["POST"])
@login_required
def manage_profile_update_password():
    if request.method == "POST":
        # 1) Declaring variables
        cur_pw, new_pw = request.form["current-pw"], request.form["new-password"]
        err_msg = "Validation error. Please verify that all your inputs matches the requirements"
        auth_msg = "Authentication failed. Incorrect password"
        success_msg = "Update success. Password updated, please re-login to verify yourself"

        # 2) Validating inputs
        if not auth_manager.validate_password_MatchFormat(cur_pw) or not auth_manager.validate_password_MatchFormat(
                new_pw):
            session["profile_manage_auth_status"] = ["null", err_msg, "alert-danger"]
            return redirect(url_for('profile_bp.manage_profile'))

        # 3) Get account from db
        data = auth_manager.get_password(current_user.id)
        if data == -1: abort(500)

        pw, salt = data[0], data[1]

        # 4) Compare input pw to db pw
        cur_pw_hash = auth_manager.hash(cur_pw, salt)
        if cur_pw_hash != pw:
            session["profile_manage_auth_status"] = ["null", auth_msg, "alert-danger"]
            return redirect(url_for('profile_bp.manage_profile'))

        # 5) Generate new salt n new hash
        new_salt = auth_manager.generate_salt()
        hash_pw = auth_manager.hash(new_pw, new_salt)

        # 6) Update password
        update_password = auth_manager.update_password_by_id(current_user.id, hash_pw, new_salt)
        if update_password == -1: abort(500)

        # Log authentication
        auth_logger_info.info("User " + current_user.id + " successfully changed his/her password")

        session.clear()
        logout_user()

        session["login_auth_status"] = ["null", success_msg, "alert-success"]
        return redirect(url_for('auth_bp.login'))
    else:
        abort(404)


# -----------------------------------------------------------------------

@auth_bp.route('/auth/management/update_tfa', methods=["POST"])
@login_required
def manage_profile_update_tfa():
    if request.method == "POST":
        # 1) Declaring variables
        tfa = request.form['tfa']
        err_msg = "Something went wrong, please try again"
        success_msg = "Update success. Email two-factor authentication have been updated"

        # 2) Validating tfa
        if tfa != '1' and tfa != '0':
            session["profile_manage_auth_status"] = ["null", err_msg, "alert-danger"]
            return redirect(url_for('profile_bp.manage_profile'))

        update_tfa = auth_manager.update_tfa(current_user.id, tfa)
        if update_tfa == -1: abort(500)

        if tfa == '1':
            # Log authentication
            auth_logger_info.info("User " + current_user.id + " enabled his/her email 2fa settings")
        elif tfa == '0':
            # Log authentication
            auth_logger_info.info("User " + current_user.id + " disabled his/her email 2fa settings")

        session["profile_manage_auth_status"] = ["null", success_msg, "alert-success"]
        return redirect(url_for('profile_bp.manage_profile'))
    else:
        abort(404)


@auth_bp.route('/auth/logout', methods=["GET"])
@login_required
def logout():
    if request.method == "GET":
        auth_logger_info.info("User " + current_user.id + " has logged out of the application")

        logout_user()
        session.clear()
        return redirect(url_for('home_bp.home'))
    else:
        abort(500)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('auth_bp.login'))


@login_manager.user_loader
def load_user(id):
    u = auth_manager.load_user(id)
    if u is None: return None

    return User(u[1], id, u[2])
