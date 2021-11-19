# Importing open-source API(s)
from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.exceptions import abort

# Importing required dependencies (Within own domain)
from Bluedit.admin.models.AdminManager import AdminManager
from Bluedit.log import admin_logger

admin_bp = Blueprint('admin_bp', __name__, template_folder="templates")
admin_manager = AdminManager()


@admin_bp.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    if current_user.role == "admin":
        if request.method == "GET":
            status = ["none", None, "alert-danger"] if session.get("admin_promote_status") is None else session.get(
                "admin_promote_status")

            session.pop('admin_promote_status', None)

            user_list = admin_manager.get_user()
            if user_list == -1:
                abort(500)
            elif not user_list:
                return render_template("admin.html", users=None, status=status)

            return render_template("admin.html", users=user_list, status=status)
        elif request.method == "POST":
            user_id = request.form['id']

            if not admin_manager.validate_input_NoSpecialCharacters(user_id):
                session['admin_promote_status'] = ["null", "Validation failed. User ID is not valid", "alert-danger"]
                return redirect(url_for("admin_bp.admin"))

            promote_user = admin_manager.promote_user(user_id)
            if promote_user == -1: abort(500)

            admin_logger.info("Admin " + current_user.id + " promoted user " + user_id + " to an admin")

            session['admin_promote_status'] = ["null", "Promote success. That user is now an admin", "alert-success"]
            return redirect(url_for("admin_bp.admin"))
        else:
            abort(404)
    else:
        return redirect(url_for('home_bp.home'))


@admin_bp.route('/admin/reported_post', methods=["GET", "POST"])
@login_required
def admin_reported_post():
    if current_user.role == 'admin':
        if request.method == "GET":
            status = ["none", None, "alert-danger"] if session.get(
                "admin_reported_post_status") is None else session.get(
                "admin_reported_post_status")

            session.pop('admin_reported_post_status', None)

            reported_post_list = admin_manager.get_reported_post()
            if reported_post_list == -1:
                abort(500)
            elif not reported_post_list:
                return render_template("admin_reported_post.html", status=status, posts=None)

            lock_list = admin_manager.get_locked_post()
            if lock_list == -1:
                abort(500)
            elif not lock_list:
                return render_template("admin_reported_post.html", status=status, posts=reported_post_list, locks=None)

            return render_template("admin_reported_post.html", status=status, posts=reported_post_list, locks=lock_list)
        elif request.method == "POST":
            post_id = request.form['id']

            if not admin_manager.validate_input_NoSpecialCharacters(post_id):
                session['admin_reported_post_status'] = ["null", "Validation failed. Post ID is not valid",
                                                         "alert-danger"]
                return redirect(url_for("admin_bp.admin_reported_post"))

            check_post_lock = admin_manager.check_post_lock_status(post_id)
            if check_post_lock == -1:
                abort(500)
            elif check_post_lock == -2:
                session['admin_reported_post_status'] = ["null", "Lock failed. Post does not exist", "alert-danger"]
                return redirect(url_for("admin_bp.admin_reported_post"))

            if not check_post_lock:
                lock_post = admin_manager.lock_post(post_id)
                if lock_post == -1: abort(500)

                admin_logger.info("Admin " + current_user.id + " locked post " + post_id)
            else:
                unlock_post = admin_manager.unlock_post(post_id)
                if unlock_post == -1: abort(500)

                admin_logger.info("Admin " + current_user.id + " unlocked post " + post_id)

            session['admin_reported_post_status'] = ["null", "Lock success. That post is now locked/unlocked",
                                                     "alert-success"]
            return redirect(url_for("admin_bp.admin_reported_post"))
        else:
            abort(404)
    else:
        return redirect(url_for('home_bp.home'))


@admin_bp.route('/admin/reported_reply', methods=["GET"])
@login_required
def admin_reported_reply():
    if current_user.role == 'admin':
        if request.method == "GET":
            status = ["none", None, "alert-danger"] if session.get("admin_reported_reply_status") is None else session.get(
                "admin_reported_reply_status")

            session.pop('admin_reported_reply_status', None)

            reported_reply_list = admin_manager.get_reported_reply()
            if reported_reply_list == -1:
                abort(500)
            elif not reported_reply_list:
                return render_template("admin_reported_reply.html", status=status, replies=None)

            return render_template("admin_reported_reply.html", status=status, replies=reported_reply_list)
        else:
            abort(404)
    else:
        return redirect(url_for('home_bp.home'))


@admin_bp.route('/admin/account_ban', methods=["GET", "POST"])
@login_required
def admin_account_ban():
    if current_user.role == 'admin':
        if request.method == "GET":
            status = ["none", None, "alert-danger"] if session.get("admin_ban_status") is None else session.get(
                "admin_ban_status")

            session.pop('admin_ban_status', None)

            user_list = admin_manager.get_all_user()
            if user_list == -1:
                abort(500)
            elif not user_list:
                return render_template("admin.html", users=None, status=status)

            get_banned_list = admin_manager.get_ban_list()
            if get_banned_list == -1:
                abort(500)
            elif not get_banned_list:
                return render_template("admin_account_ban.html", users=user_list, status=status, banned=None)

            return render_template("admin_account_ban.html", users=user_list, status=status, banned=get_banned_list)
        elif request.method == "POST":
            user_id = request.form['id']

            if not admin_manager.validate_input_NoSpecialCharacters(user_id):
                session['admin_ban_status'] = ["null", "Validation failed. User ID is not valid",
                                               "alert-danger"]
                return redirect(url_for("admin_bp.admin_account_ban"))

            check_ban_status = admin_manager.check_ban_status(user_id)
            if check_ban_status == -1:
                abort(500)
            elif check_ban_status == -2:
                session['admin_ban_status'] = ["null", "Ban failed. User does not exist", "alert-danger"]
                return redirect(url_for("admin_bp.admin_account_ban"))

            if not check_ban_status:
                ban_user = admin_manager.ban_user(user_id)
                if ban_user == -1: abort(500)

                admin_logger.info("Admin " + current_user.id + " banned user " + user_id)
            else:
                unban_user = admin_manager.unban_user(user_id)
                if unban_user == -1: abort(500)

                admin_logger.info("Admin " + current_user.id + " unbanned user " + user_id)

            session['admin_ban_status'] = ["null", "Ban success. That user is now banned/unbanned",
                                           "alert-success"]
            return redirect(url_for("admin_bp.admin_account_ban"))
        else:
            abort(404)
    else:
        return redirect(url_for('home_bp.home'))
