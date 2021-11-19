# Importing open-source API(s)
from flask import Blueprint, render_template, request, session, redirect, url_for

# Importing required dependencies (Within own domain)
from flask_login import current_user
from werkzeug.exceptions import abort

from Bluedit.home.models.HomeManager import HomeManager
from Bluedit.home.models.PostSearch import PostSearch
from Bluedit.home.models.PostSort import PostSort

home_bp = Blueprint('home_bp', __name__, template_folder="templates")
home_manager = HomeManager()
post_searcher = PostSearch()
post_sorter = PostSort()


@home_bp.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        search = session.get("post_search")
        valid_target = ["1", "2", "3", "4", "5", "6", "7", "8"]
        session.pop("post_search", None)

        if search is None:
            post_collections = home_manager.get_all_post()
            if post_collections == -1: abort(500)
        else:
            post_collections = post_searcher.select_search_method(search[0], search[1])
            if post_collections == -1: abort(500)

        # Get like & save list of current user
        if current_user.is_authenticated:
            like_list = home_manager.get_like_list_by_userid(current_user.id)
            if like_list == -1: abort(500)
            save_list = home_manager.get_save_list_by_userid(current_user.id)
            if save_list == -1: abort(500)
        else:
            like_list = []
            save_list = []

        if request.args.get('sort') is not None:
            id = request.args.get('sort')
            if id in valid_target:
                post_collections = post_sorter.select_sort_method(id, post_collections)
                return render_template('home.html', posts=post_collections, id=id, likes=like_list, saves=save_list)

        return render_template('home.html', posts=post_collections, likes=like_list, saves=save_list)
    elif request.method == "POST":
        # 1) Defining Variables
        search_target, search_value = request.form['category'], request.form['search_target']
        valid_target = ["postTitle", "postContent", "UUID", "postCat"]

        # 2) Validating inputs
        if search_target not in valid_target:
            return redirect(url_for('home_bp.home'))
        if not home_manager.validate_input_NoSpecialCharacters(search_value):
            return redirect(url_for('home_bp.home'))

        # 3) Saving values
        session["post_search"] = [search_target, search_value]
        return redirect(url_for('home_bp.home'))
    else:
        abort(500)
