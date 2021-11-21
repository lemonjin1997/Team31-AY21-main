# Importing open-source API(s)
import hashlib

from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

# Importing required dependencies (Within own domain)
from Bluedit.profile.models.ProfileManager import ProfileManager

# Importing required dependencies (From shared)
from config import Config
from Bluedit.log import error_logger, user_logger

# Import python build-in libraries
import html

profile_bp = Blueprint('profile_bp', __name__, template_folder='templates')
profile_manager = ProfileManager()


@profile_bp.route('/profile/user/<name>')
def profile(name):
    if request.method == "GET":
        status = ["none", None, "alert-danger"] if session.get("profile_auth_status") is None else session.get(
            "profile_auth_status")

        session.pop("profile_auth_status", None)

        # 1) Validate name (from url or form)
        if not profile_manager.validate_input_NoSpecialCharacters(name):
            return render_template("profile.html", user=name, name_valid=False, status=status)

        # 2) Check if name exist
        name_exist = profile_manager.name_exist(name)
        if name_exist == -1:
            abort(500)
        elif not name_exist:
            return render_template("profile.html", user=name, name_valid=False, status=status)

        # 3) Get profile datas
        profile = profile_manager.get_profile(name)
        if profile == -1:
            abort(500)
        elif profile == -2:
            return render_template("profile.html", user=name, name_valid=False, status=status)

        # 4) Get profile posted data
        posts = profile_manager.get_user_post_top_3(name)
        if posts == -1: abort(500)

        if len(posts) == 0:
            posts = None

        # 5) Reconvert html encoding back to symbols
        profile.about = html.unescape(profile.about)

        # 6) Check if this profile is mine
        if current_user.is_authenticated:
            if current_user.name == name:
                return render_template("profile.html", user=name, name_valid=True, my_profile=True, profile=profile,
                                       status=status, posts=posts)

        return render_template("profile.html", user=name, name_valid=True, my_profile=False, profile=profile,
                               status=status, posts=posts)
    else:
        abort(404)


@profile_bp.route('/profile/search', methods=["POST"])
def search_profile():
    if request.method == "POST":
        # No validation or sanitization needed, the check is handled by the profile page itself
        name = request.form["username"]
        return redirect(url_for('profile_bp.profile', name=name))
    else:
        abort(404)


@profile_bp.route('/profile/image_change', methods=["POST"])
@login_required
def image_change():
    if request.method == "POST":
        # 1) Detect if file exist in stream
        if request.files["image"].filename != '':
            # 2) Declare Variables
            image = request.files["image"]
            filename = secure_filename(image.filename)

            folder_identity = hashlib.sha1(str(current_user.id).encode()).hexdigest()   #nosec

            image_folder = Config.IMAGE_UPLOADS + "profile_image/" + str(folder_identity)
            fail_msg = "Update failed. Please ensure file is valid"
            success_msg = "Update success. Profile image have been updated"

            # 2) File validations
            filename_empty = profile_manager.validate_filename_not_empty(filename)
            filename_valid = profile_manager.validate_filename_valid(filename)
            filename_extension = profile_manager.validate_file_extension(filename)

            if not filename_extension:
                error_logger.error(
                    "Encountered error while uploading file - 422 Request Entity Invalid Format: The file detected is not in a valid format.")

            if not filename_empty or not filename_valid or not filename_extension:
                session["profile_auth_status"] = ["null", fail_msg, "alert-danger"]
                return redirect(url_for("profile_bp.profile", name=current_user.name))

            # 2) Set a folder in the server
            set_image_folder = profile_manager.set_profile_image_folder(image_folder, image, filename)
            if not set_image_folder:
                session["profile_auth_status"] = ["null", fail_msg, "alert-danger"]
                return redirect(url_for("profile_bp.profile", name=current_user.name))

            # 2) Store the folder path to db
            store_path = "../../" + image_folder + "/" + filename
            update_image_path = profile_manager.update_user_image_path(store_path, current_user.name, current_user.id)
            if update_image_path == -1: abort(500)

            user_logger.info(
                "User " + current_user.id + "updated his/her profile image. File is stored at - " + store_path)

            session["profile_auth_status"] = ["null", success_msg, "alert-success"]
        else:
            fail_msg = "Update failed. Please ensure that you have selected a file"
            session["profile_auth_status"] = ["null", fail_msg, "alert-danger"]

        return redirect(url_for("profile_bp.profile", name=current_user.name))
    else:
        abort(404)


@profile_bp.route('/profile/management', methods=["GET"])
@login_required
def manage_profile():
    if request.method == "GET":
        auth_msg = "Authentication failed. Please re-login to initiate the verification process"
        status = ["none", None, "alert-danger"] if session.get("profile_manage_auth_status") is None else session.get(
            "profile_manage_auth_status")

        session.pop("profile_manage_auth_status", None)

        email_auth = profile_manager.get_user_fa_status(current_user.id)
        if email_auth == -1: abort(500)

        profile = profile_manager.get_profile(current_user.name)
        if profile == -1:
            abort(500)
        elif profile == -2:
            session["login_auth_status"] = ["null", auth_msg, "alert-danger"]
            return redirect(url_for("auth_bp.login"))

        profile.about = html.unescape(profile.about)

        return render_template("profile_management.html", profile=profile, status=status, email_auth=email_auth)
    else:
        abort(404)


@profile_bp.route('/profile/management/update_name', methods=["POST"])
@login_required
def manage_profile_update_name():
    if request.method == "POST":
        uname = request.form["username"]
        no_change_msg = "No Update. Input name is similar to current name"
        err_msg = "Update failed. Please check that you have inputted a valid username"
        exist_msg = "Update failed. Username is already in use"
        success_msg = "Update success. Username have been updated"

        # 1) check if input name is similar to current name
        if uname == current_user.name:
            session["profile_manage_auth_status"] = ["null", no_change_msg, "alert-success"]
            return redirect(url_for('profile_bp.manage_profile'))

        # 2) Validate input name
        if not profile_manager.validate_input_NoSpecialCharacters(uname):
            session["profile_manage_auth_status"] = ["null", err_msg, "alert-danger"]
            return redirect(url_for('profile_bp.manage_profile'))

        # 3) Check if name exist
        name_exist = profile_manager.name_exist(uname)
        if name_exist:
            session["profile_manage_auth_status"] = ["null", exist_msg, "alert-danger"]
            return redirect(url_for('profile_bp.manage_profile'))

        # 4) Update username
        update_username = profile_manager.update_username(current_user.name, uname, current_user.id)
        if update_username == -1: abort(500)

        user_logger.info(
            "User " + current_user.id + "updated his/her username from " + current_user.name + " to " + uname)

        current_user.name = uname
        session["profile_manage_auth_status"] = ["null", success_msg, "alert-success"]
        return redirect(url_for('profile_bp.manage_profile'))
    else:
        abort(404)


@profile_bp.route('/profile/management/update_about', methods=["POST"])
@login_required
def manage_profile_update_about():
    if request.method == "POST":
        about = request.form["about"]
        success_msg = "Update success. About have been updated"

        # 1) convert about (all symbol to html encoding)
        about = profile_manager.validate_text_replaceSymbol(about)

        # 2) update user about
        update_about = profile_manager.update_about(current_user.name, current_user.id, about)
        if update_about == -1: about(500)

        user_logger.info("User " + current_user.id + "updated his/her about information")

        session["profile_manage_auth_status"] = ["null", success_msg, "alert-success"]
        return redirect(url_for('profile_bp.manage_profile'))
    else:
        abort(404)


@profile_bp.route('/profile/personal/my_post', methods=["GET"])
@login_required
def profile_mypost():
    if request.method == "GET":
        if current_user.is_authenticated:
            user_post = profile_manager.get_user_post(current_user.name)
            if user_post == -1: abort(500)

            if len(user_post) == 0: user_post = None
            return render_template("profile_mypost.html", posts=user_post)
        else:
            return redirect(url_for('home_bp.home'))
    else:
        abort(404)


@profile_bp.route('/profile/personal/my_stash', methods=["GET"])
@login_required
def profile_mystash():
    if request.method == "GET":
        if current_user.is_authenticated:
            stash_post = profile_manager.get_stashed_post(current_user.id)
            if stash_post == -1: abort(500)

            # Get like & save list of current user
            if current_user.is_authenticated:
                like_list = profile_manager.get_like_list_by_userid(current_user.id)
                if like_list == -1: abort(500)
                save_list = profile_manager.get_save_list_by_userid(current_user.id)
                if save_list == -1: abort(500)
            else:
                like_list = []
                save_list = []

            if len(stash_post) == 0: stash_post = None
            return render_template("profile_mystash.html", posts=stash_post, likes=like_list, saves=save_list)
        else:
            return redirect(url_for('home_bp.home'))
    else:
        abort(404)


@profile_bp.route('/profile/personal/my_upvote', methods=["GET"])
@login_required
def profile_myupvote():
    if request.method == "GET":
        if current_user.is_authenticated:
            upvote_post = profile_manager.get_upvote_post(current_user.id)
            if upvote_post == -1: abort(500)

            # Get like & save list of current user
            if current_user.is_authenticated:
                like_list = profile_manager.get_like_list_by_userid(current_user.id)
                if like_list == -1: abort(500)
                save_list = profile_manager.get_save_list_by_userid(current_user.id)
                if save_list == -1: abort(500)
            else:
                like_list = []
                save_list = []

            if len(upvote_post) == 0: upvote_post = None
            return render_template("profile_myupvote.html", posts=upvote_post, likes=like_list, saves=save_list)
        else:
            return redirect(url_for('home_bp.home'))
    else:
        abort(404)


@profile_bp.route('/profile/personal/my_upvote/reply', methods=["GET"])
@login_required
def profile_myupvote_reply():
    if request.method == "GET":
        if current_user.is_authenticated:
            upvote_reply = profile_manager.get_upvote_reply(current_user.id)
            if upvote_reply == -1: abort(500)

            # Get like & save list of current user
            if current_user.is_authenticated:
                r_like_list = profile_manager.get_r_like_list_by_userid(current_user.id)
                if r_like_list == -1: abort(500)
            else:
                r_like_list = []

            if len(upvote_reply) == 0: upvote_reply = None
            return render_template("profile_myupvote_reply.html", replies=upvote_reply, r_likes=r_like_list)
        else:
            return redirect(url_for('home_bp.home'))
    else:
        abort(404)


@profile_bp.route('/profile/personal/my_comment', methods=["GET"])
@login_required
def profile_mycomment():
    if request.method == "GET":
        if current_user.is_authenticated:
            comments = profile_manager.get_commented_post(current_user.id)
            if comments == -1: abort(500)

            # Get like & save list of current user
            if current_user.is_authenticated:
                r_like_list = profile_manager.get_r_like_list_by_userid(current_user.id)
                if r_like_list == -1: abort(500)
            else:
                r_like_list = []

            if len(comments) == 0: comments = None
            return render_template("profile_mycomment.html", replies=comments, r_likes=r_like_list)
        else:
            return redirect(url_for('home_bp.home'))
    else:
        abort(404)
