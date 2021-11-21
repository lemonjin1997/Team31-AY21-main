from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from config import Config
from Bluedit.log import error_logger, post_logger, admin_logger

from Bluedit.post.models.PostManager import PostManager

post_bp = Blueprint('post_bp', __name__, template_folder="templates")
post_manager = PostManager()


@post_bp.route('/post/post_form', methods=["GET", "POST"])
@login_required
def post_form():
    if request.method == "GET":
        status = ["none", None, "alert-danger"] if session.get("post_form_status") is None else session.get(
            "post_form_status")
        session.pop("post_form_status", None)

        return render_template("post_form.html", status=status)
    elif request.method == "POST":
        # 1) Declare variables
        title, content = request.form['title'], request.form['content']
        cat = ["default"] if request.form['categories'] == '' else request.form['categories']
        filename = "No Image" if request.files['image'].filename == '' else secure_filename(
            request.files['image'].filename)
        image_folder = Config.IMAGE_UPLOADS + "post_image/"
        validate_msg = "Validation failed. Please ensure that all your inputs are in the correct format"

        # 2) Validating inputs
        if not post_manager.validate_post_title(title):
            session["post_form_status"] = ["null", validate_msg, "alert-danger"]
            return redirect(url_for("post_bp.post_form"))

        replaced_content = post_manager.validate_text_replaceSymbol(content)

        if cat[0] != "default":
            if not post_manager.validate_post_category(cat):
                session["post_form_status"] = ["null", validate_msg, "alert-danger"]
                return redirect(url_for("post_bp.post_form"))

            cat = list(filter(None, str(cat).replace(" ", "").split(";")))

        if filename != "No Image":
            filename_not_empty = post_manager.validate_filename_not_empty(filename)
            filename_valid = post_manager.validate_filename_valid(filename)
            filename_ext_valid = post_manager.validate_file_extension(filename)

            if not filename_ext_valid:
                error_logger.error(
                    "Encountered error while uploading file - 422 Request Entity Invalid Format: The file detected is not in a valid format.")

            if not filename_not_empty or not filename_valid or not filename_ext_valid:
                session["post_form_status"] = ["null", validate_msg, "alert-danger"]
                return redirect(url_for("post_bp.post_form"))

            # 3) Save img to folder
            full_path = post_manager.add_image_to_folder(image_folder, filename, request.files['image'])
            db_img_path = "../../" + full_path
        else:
            db_img_path = filename

        upload_post = post_manager.upload_post(title, replaced_content, cat, db_img_path, current_user.id)
        if upload_post == -1: abort(500)

        post_logger.info("User " + current_user.id + " posted a new post - post ID " + upload_post)

        return redirect(url_for("home_bp.home"))
    else:
        abort(404)


@post_bp.route('/post/<postid>', methods=["GET", "POST"])
def post_data(postid):
    if request.method == "GET":
        status = ["none", None, "alert-danger"] if session.get("comment_auth_status") is None else session.get(
            "comment_auth_status")

        session.pop("comment_auth_status", None)

        post = post_manager.get_post(postid)
        if post == -1:
            abort(500)
        elif post == -2:
            return redirect(url_for('home_bp.home'))

        # Get like & save & reply_like list of current user
        if current_user.is_authenticated:
            like_list = post_manager.get_like_list_by_userid(current_user.id)
            if like_list == -1: abort(500)
            save_list = post_manager.get_save_list_by_userid(current_user.id)
            if save_list == -1: abort(500)
            r_like_list = post_manager.get_r_like_list_by_userid(current_user.id)
            if r_like_list == -1: abort(500)
        else:
            like_list = []
            save_list = []
            r_like_list = []

        get_lock_status = post_manager.get_postlock_status(postid)
        if get_lock_status == -1:
            abort(500)
        elif get_lock_status == -2:
            return redirect(url_for('home_bp.home'))

        replies = post_manager.get_replies(postid)
        if replies == -1:
            abort(500)
        elif replies == -2:
            return render_template('post_main.html', post=post, status=status, replies=None, likes=like_list,
                                   saves=save_list, r_likes=r_like_list, locked=get_lock_status)

        return render_template('post_main.html', post=post, status=status, replies=replies, likes=like_list,
                               saves=save_list, r_likes=r_like_list, locked=get_lock_status)
    elif request.method == "POST":
        # 1) validate user is login
        if not current_user.is_authenticated:
            return redirect(url_for('auth_bp.login'))

        # 2) Declare Variables
        comment = request.form['content']
        validation_fail_msg = "- Validation failed. Please input something into the comment before submitting"
        comment_succ = "- Comment Successful. Your comment have been uploading"

        # 3) Validating variables
        if len(comment) <= 0:
            session["comment_auth_status"] = ["null", validation_fail_msg, "alert-danger"]
            return redirect(url_for('post_bp.post_data', postid=postid))

        replaced_comment = post_manager.validate_text_replaceSymbol(comment)

        # 4) Save to db
        upload_comments = post_manager.upload_comments(postid, current_user.id, replaced_comment)
        if upload_comments == -1: abort(500)

        post_logger.info("User " + current_user.id + " replied to post " + postid + " - reply ID " + upload_comments)

        session["comment_auth_status"] = ["null", comment_succ, "alert-success"]
        return redirect(url_for('post_bp.post_data', postid=postid))
    else:
        abort(404)


@post_bp.route('/post_edit/<postid>', methods=["GET", "POST"])
@login_required
def post_edit(postid):
    if request.method == "GET":
        status = ["none", None, "alert-danger"] if session.get("postedit_auth_status") is None else session.get(
            "postedit_auth_status")

        session.pop("postedit_auth_status", None)

        target_post = post_manager.get_post(postid)
        if target_post == -1:
            abort(500)
        elif target_post == -2:
            return redirect(url_for("profile_bp.profile_mypost"))

        return render_template("post_editpost.html", status=status, post=target_post)
    elif request.method == "POST":
        title, content = request.form['title'], request.form['content']
        validation_err_msg = "Validation failed. Please verify your inputs"

        if not post_manager.validate_post_title(title):
            session["postedit_auth_status"] = ["null", validation_err_msg, "alert-danger"]

        updated_content = post_manager.validate_text_replaceSymbol(content)

        update_post = post_manager.update_post(postid, title, updated_content)
        if update_post == -1: abort(500)

        post_logger.info("User " + current_user.id + " updated post " + postid)

        return redirect(url_for("profile_bp.profile_mypost"))
    else:
        abort(404)


@post_bp.route('/reply_edit/<replyid>', methods=["GET", "POST"])
@login_required
def reply_edit(replyid):
    if request.method == "GET":
        status = ["none", None, "alert-danger"] if session.get("replyedit_auth_status") is None else session.get(
            "replyedit_auth_status")

        session.pop("replyedit_auth_status", None)

        reply = post_manager.get_reply_by_replyid(replyid)
        if reply == -1:
            abort(500)
        elif reply == -2:
            return redirect(url_for("profile_bp.profile_mycomment"))

        return render_template("post_editreply.html", status=status, reply=reply)
    elif request.method == "POST":
        content = request.form['content']

        replaced_content = post_manager.validate_text_replaceSymbol(content)

        update_reply = post_manager.update_reply(replyid, replaced_content)
        if update_reply == -1: abort(500)

        post_logger.info("User " + current_user.id + " updated reply " + replyid)

        return redirect(url_for("profile_bp.profile_mycomment"))
    else:
        abort(404)


@post_bp.route('/post_report/<postid>', methods=["POST"])
@login_required
def post_report(postid):
    if request.method == "POST":
        if not post_manager.validate_input_NoSpecialCharacters(postid):
            return redirect(url_for('home_bp.home'))

        post_exist = post_manager.check_post_exist(postid)
        if post_exist == -1:
            return abort(500)
        elif post_exist == 0:
            return redirect(url_for('home_bp.home'))

        if current_user.is_authenticated:
            reported_before = post_manager.check_report_list(postid, current_user.id)
            if reported_before == -1: abort(500)
            if reported_before: return redirect(url_for('home_bp.home'))

            report_post = post_manager.report_post(postid, current_user.id)
            if report_post == -1: abort(500)

            post_logger.info("User " + current_user.id + " reported post " + postid)

        return redirect(url_for('home_bp.home'))
    else:
        abort(404)


@post_bp.route('/reply_report/<replyid>', methods=["POST"])
@login_required
def reply_report(replyid):
    if request.method == "POST":
        if not post_manager.validate_input_NoSpecialCharacters(replyid):
            return redirect(url_for('home_bp.home'))

        reply_exist = post_manager.check_reply_exist(replyid)
        if reply_exist == -1:
            return abort(500)
        elif reply_exist == 0:
            return redirect(url_for('home_bp.home'))

        if current_user.is_authenticated:
            reported_before = post_manager.check_reply_report_list(replyid, current_user.id)
            if reported_before == -1: abort(500)
            if reported_before: return redirect(url_for('home_bp.home'))

            report_reply = post_manager.report_reply(replyid, current_user.id)
            if report_reply == -1: abort(500)

            post_logger.info("User " + current_user.id + " reported reply " + replyid)

        return redirect(url_for('home_bp.home'))
    else:
        abort(404)


@post_bp.route('/post_like/<postid>', methods=["POST"])
def post_like(postid):
    if request.method == "POST":
        if not current_user.is_authenticated:
            return jsonify(-2), 200

        validate_id = post_manager.validate_input_NoSpecialCharacters(postid)
        if not validate_id:
            return jsonify(-3), 200

        validate_post_exist = post_manager.check_post_exist(postid)
        if validate_post_exist == -1:
            return jsonify(-1), 200
        elif validate_post_exist == 0:
            return jsonify(-3), 200

        liked = False

        # 1) Get list of liked user for the post
        post_like_list = post_manager.get_like_list(postid)
        if post_like_list == -1:
            return jsonify(-1), 200

        # 2) Check if user already like the post
        for data in post_like_list:
            if current_user.id in data:
                liked = True
                break

        # 3) Like the post
        if not liked:
            like_post = post_manager.like_post(postid, current_user.id)
            if like_post == -1:
                return jsonify(-1), 200

            post_logger.info("User " + current_user.id + " liked post " + postid)
        elif liked:
            dislike_post = post_manager.dislike_post(postid, current_user.id)
            if dislike_post == -1:
                return jsonify(-1), 200

            post_logger.info("User " + current_user.id + " unliked post " + postid)

        return jsonify(1), 200
    else:
        return jsonify(-1), 200


@post_bp.route('/post_save/<postid>', methods=["POST"])
def post_save(postid):
    if request.method == "POST":
        if not current_user.is_authenticated:
            return jsonify(-2), 200

        validate_id = post_manager.validate_input_NoSpecialCharacters(postid)
        if not validate_id:
            return jsonify(-3), 200

        validate_post_exist = post_manager.check_post_exist(postid)
        if validate_post_exist == -1:
            return jsonify(-1), 200
        elif validate_post_exist == 0:
            return jsonify(-3), 200

        saved = False

        # 1) Get list of save user for the post
        post_save_stash = post_manager.get_save_stash(postid)
        if post_save_stash == -1:
            return jsonify(-1), 200

        # 2) Check if user already save the post
        for data in post_save_stash:
            if current_user.id in data:
                saved = True
                break

        # 3) save the post
        if not saved:
            save_post = post_manager.save_post(postid, current_user.id)
            if save_post == -1:
                return jsonify(-1), 200

            post_logger.info("User " + current_user.id + " saved post " + postid)
        elif saved:
            unsave_post = post_manager.unsave_post(postid, current_user.id)
            if unsave_post == -1:
                return jsonify(-1), 200

            post_logger.info("User " + current_user.id + " unsaved post " + postid)

        return jsonify(1), 200
    else:
        return jsonify(-1), 200


@post_bp.route('/reply_like/<replyid>', methods=["POST"])
def reply_like(replyid):
    if request.method == "POST":
        if not current_user.is_authenticated:
            return jsonify(-2), 200

        validate_id = post_manager.validate_input_NoSpecialCharacters(replyid)
        if not validate_id:
            return jsonify(-3), 200

        validate_reply_exist = post_manager.check_reply_exist(replyid)
        if validate_reply_exist == -1:
            return jsonify(-1), 200
        elif validate_reply_exist == 0:
            return jsonify(-3), 200

        liked = False

        # 1) Get list of save user for the post
        reply_like_list = post_manager.get_rlike_stash(replyid)
        if reply_like_list == -1:
            return jsonify(-1), 200

        # 2) Check if user already save the post
        for data in reply_like_list:
            if current_user.id in data:
                liked = True
                break

        # 3) save the post
        if not liked:
            like_reply = post_manager.like_reply(replyid, current_user.id)
            if like_reply == -1:
                return jsonify(-1), 200

            post_logger.info("User " + current_user.id + " liked reply " + replyid)
        elif liked:
            unlike_reply = post_manager.unlike_reply(replyid, current_user.id)
            if unlike_reply == -1:
                return jsonify(-1), 200

            post_logger.info("User " + current_user.id + " unliked reply " + replyid)

        return jsonify(1), 200
    else:
        return jsonify(-1), 200


@post_bp.route('/delete_post/<postid>', methods=["POST"])
@login_required
def delete_post(postid):
    if request.method == "POST":
        my_post = post_manager.check_post_is_mine(postid, current_user.id)
        if my_post == -1:
            abort(500)
        elif my_post == 0:
            return redirect(url_for("home_bp.home"))

        delete_post = post_manager.delete_post_by_id(postid, current_user.id)
        if delete_post == -1: abort(500)

        post_logger.info("User " + current_user.id + " deleted post " + postid)

        return redirect(url_for("home_bp.home"))
    else:
        abort(404)


@post_bp.route('/delete_reply/<replyid>', methods=["POST"])
@login_required
def delete_reply(replyid):
    if request.method == "POST":
        print(replyid)
        my_reply = post_manager.check_reply_is_mine(replyid, current_user.id)
        if my_reply == -1:
            abort(500)
        elif my_reply == 0:
            return redirect(url_for("home_bp.home"))

        delete_reply = post_manager.delete_reply_by_id(replyid, current_user.id)
        if delete_reply == -1: abort(500)

        post_logger.info("User " + current_user.id + " deleted reply " + replyid)

        return redirect(url_for("home_bp.home"))
    else:
        abort(404)


@post_bp.route('/admin/delete_post/<postid>', methods=["POST"])
@login_required
def delete_post_admin(postid):
    if current_user.role == 'admin':
        if request.method == "POST":
            delete_post = post_manager.delete_post(postid)
            if delete_post == -1: abort(500)

            admin_logger.info("Admin " + current_user.id + " deleted post " + postid)

            return redirect(url_for("home_bp.home"))
        else:
            abort(404)
    else:
        return redirect(url_for('admin_bp.admin_reported_post'))


@post_bp.route('/admin/delete_reply/<replyid>', methods=["POST"])
@login_required
def delete_reply_admin(replyid):
    if current_user.role == 'admin':
        if request.method == "POST":
            delete_reply = post_manager.delete_reply(replyid)
            if delete_reply == -1: abort(500)

            admin_logger.info("Admin " + current_user.id + " deleted reply " + replyid)

            return redirect(url_for("home_bp.home"))
        else:
            abort(404)
    else:
        return redirect(url_for('admin_bp.admin_reported_reply'))
