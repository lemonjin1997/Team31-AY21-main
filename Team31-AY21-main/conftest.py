import datetime

import pytest
from unittest.mock import patch
from Bluedit.auth.models.User import User
from Bluedit.auth.models.Account import Account
from Bluedit.home.models.PostSearch import PostSearch
from Bluedit.post.models.PostManager import PostManager
from Bluedit.home.models.HomeManager import HomeManager
from Bluedit.admin.models.AdminManager import AdminManager
from Bluedit.auth.models.AccountManager import AccountManager
from Bluedit.profile.models.ProfileManager import ProfileManager


@pytest.fixture()
def user():
    u = User("test_name", 123, "test_user")
    return u


@pytest.fixture()
def account():
    a = Account("testid", "testemail", "testpassword", "testsalt", "testdate", 1, 1, 1, "testkey", "test_pwdate")
    return a


@pytest.fixture()
def mocked_load_user_dbwithresult():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_id_name_role_by_id', return_value=(("some_result"),)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_load_user_dberror():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_id_name_role_by_id', return_value="some error message"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_exist_otpkey_error():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_exist_otpkey', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_exist_otpkey_Pass():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_exist_otpkey', return_value=(0,)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_get_account_by_email_dberror():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_account_by_email', return_value="some error message"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_get_account_by_email_dbnoresult():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_account_by_email', return_value=()):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_get_account_by_email_dbresult():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_account_by_email', return_value=(
            "testid", "testemail", "testpassword", "testsalt", 1, "testdate", "", 1, 1, "testkey", "test_pwdate")):
        result = AccountManager()
        yield result



@pytest.fixture()
def mocked_select_act_status_by_email_DBError():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_act_status_by_email', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_act_status_by_email_DBNoResult():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_act_status_by_email', return_value=()):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_act_status_by_email_DBActivated():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_act_status_by_email', return_value=(1,)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_act_status_by_email_DBNotActivated():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_act_status_by_email', return_value=(0,)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_update_act_status_by_email_DBError():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.update_act_status_by_email', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_update_act_status_by_email_DBResult():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.update_act_status_by_email', return_value=("some_value",)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_email_exist_dberror():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_exist_email', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_email_exist_dbTrue():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_exist_email', return_value=(1,)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_email_exist_dbFalse():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_exist_email', return_value=(0,)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_exist_salt_error():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_exist_salt', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_exist_salt_Pass():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_exist_salt', return_value=(0,)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_update_password_by_email_DBError():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.update_password_by_email', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_update_password_by_email_DBResult():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.update_password_by_email', return_value=("some_value",)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_username_exist_dberror():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_exist_username', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_username_exist_dbTrue():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_exist_username', return_value=(1,)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_username_exist_dbFalse():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_exist_username', return_value=(0,)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_insert_new_user_DBError():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.insert_new_user', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_otpkey_by_email_DBError():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_otpkey_by_email', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_otpkey_by_email_DBNoResult():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_otpkey_by_email', return_value=()):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_otpkey_by_email_DBResult():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_otpkey_by_email', return_value=("some_key",)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_profile_by_name_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_profile_by_name', return_value="some_error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_profile_by_name_DBNoResult():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_profile_by_name', return_value=()):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_profile_by_name_DBResult():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_profile_by_name',
               return_value=("id", "name", "about", 0, 0, 0, 0, 0, "img")):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_top3user_post_by_name_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_top3user_post_by_name',
               return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_update_image_by_nameid_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.update_image_by_nameid',
               return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_update_image_by_nameid_DBTrue():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.update_image_by_nameid',
               return_value=True):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_fa_by_id_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_fa_by_id', return_value="Some Error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_fa_by_id_DBResult():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_fa_by_id', return_value=(1,)):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_update_name_by_nameid_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.update_name_by_nameid', return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_update_name_by_nameid_DBTrue():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.update_name_by_nameid', return_value=True):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_update_about_by_nameid_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.update_about_by_nameid', return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_update_about_by_nameid_DBTrue():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.update_about_by_nameid', return_value=True):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_authenticate_email_DBError():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_authenticate_email', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_authenticate_email_DBTrue():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_authenticate_email', return_value=(1,)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_authenticate_email_DBFalse():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_authenticate_email', return_value=(0,)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_update_email_by_id_DBError():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.update_email_by_id', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_update_email_by_id_DBPass():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.update_email_by_id', return_value=True):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_update_password_by_id_DBError():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.update_password_by_id', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_update_password_by_id_DBPass():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.update_password_by_id', return_value=True):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_passwordsalt_by_id_DBError():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_passwordsalt_by_id', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_passwordsalt_by_id_DBResult():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.select_passwordsalt_by_id', return_value=("some_result",)):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_update_tfa_by_id_DBError():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.update_tfa_by_id', return_value="some_error"):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_update_tfa_by_id_DBPass():
    with patch('Bluedit.auth.auth_gateway.AccountGateway.update_tfa_by_id', return_value=True):
        result = AccountManager()
        yield result


@pytest.fixture()
def mocked_select_user_post_by_name_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_user_post_by_name', return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_stashed_post_by_id_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_stashed_post_by_id', return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_like_by_userid_DBError():
    with patch('Bluedit.home.home_gateway.HomeGateway.select_like_by_userid', return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_like_by_userid_DBNoResult():
    with patch('Bluedit.home.home_gateway.HomeGateway.select_like_by_userid', return_value=()):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_like_by_userid_DBResult():
    with patch('Bluedit.home.home_gateway.HomeGateway.select_like_by_userid', return_value=(("postid", "userid"),)):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_save_by_userid_DBError():
    with patch('Bluedit.home.home_gateway.HomeGateway.select_save_by_userid', return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_save_by_userid_DBNoResult():
    with patch('Bluedit.home.home_gateway.HomeGateway.select_save_by_userid', return_value=()):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_save_by_userid_DBResult():
    with patch('Bluedit.home.home_gateway.HomeGateway.select_save_by_userid', return_value=(("postid", "userid"),)):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_upvote_post_by_id_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_upvote_post_by_id', return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_upvoted_reply_by_id_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_upvoted_reply_by_id', return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_r_like_by_userid_DBError():
    with patch('Bluedit.home.home_gateway.HomeGateway.select_r_like_by_userid', return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_r_like_by_userid_DBNoResult():
    with patch('Bluedit.home.home_gateway.HomeGateway.select_r_like_by_userid', return_value=()):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_r_like_by_userid_DBResult():
    with patch('Bluedit.home.home_gateway.HomeGateway.select_r_like_by_userid', return_value=(("replyid", "userid"),)):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_commented_post_by_id_DBError():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_commented_post_by_id', return_value="some error"):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_commented_post_by_id_DBResult():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_commented_post_by_id',
               return_value=(("a", "b", "c", datetime.datetime(2009, 5, 5, 12, 30, 21), 1, 3, 2, 5, "some", "random",
                              "string", 2, 3, 4, 5, 6, 7, 8, 9, 2),)):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_select_commented_post_by_id_DBNoResult():
    with patch('Bluedit.profile.profile_gateway.ProfileGateway.select_commented_post_by_id',
               return_value=()):
        result = ProfileManager()
        yield result


@pytest.fixture()
def mocked_get_all_post_with_conditions_DBError():
    with patch('Bluedit.home.home_gateway.HomeGateway.get_all_post_with_conditions',
               return_value="some error"):
        result = PostSearch()
        yield result


@pytest.fixture()
def mocked_get_all_post_DBError():
    with patch('Bluedit.home.home_gateway.HomeGateway.get_all_post', return_value="some error"):
        result = PostSearch()
        yield result


@pytest.fixture()
def mocked_get_all_post_home_DBError():
    with patch('Bluedit.home.home_gateway.HomeGateway.get_all_post', return_value="some error"):
        result = HomeManager()
        yield result


@pytest.fixture()
def mocked_select_all_user_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_all_user', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_all_user_DBNoResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_all_user', return_value=()):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_all_user_DBResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_all_user',
               return_value=("time", "id", "name", "role")):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_update_userrole_by_id_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.update_userrole_by_id', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_update_userrole_by_id_DBTrue():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.update_userrole_by_id', return_value=True):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_reported_post_list_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_reported_post_list', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_reported_post_list_DBNoResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_reported_post_list', return_value=()):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_reported_post_list_DBResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_reported_post_list',
               return_value=(("id", "title", "content", 3),)):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_locked_post_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_locked_post', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_locked_post_DBNoResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_locked_post', return_value=()):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_locked_post_DBResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_locked_post', return_value=(("someid",),)):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_lockstatus_by_id_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_lockstatus_by_id', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_lockstatus_by_id_DBNoResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_lockstatus_by_id', return_value=()):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_lockstatus_by_id_DBResultLock():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_lockstatus_by_id', return_value=((1,),)):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_lockstatus_by_id_DBResultUnlock():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_lockstatus_by_id', return_value=((0,),)):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_update_postlock_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.update_postlock', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_update_postlock_DBTrue():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.update_postlock', return_value=True):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_update_postlock_unlock_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.update_postlock_unlock', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_update_postlock_unlock_DBTrue():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.update_postlock_unlock', return_value=True):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_reported_reply_list_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_reported_reply_list', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_reported_reply_list_DBNoResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_reported_reply_list', return_value=()):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_reported_reply_list_DBResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_reported_reply_list',
               return_value=(("id", "content", 3),)):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_all_user_by_auth_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_all_user_by_auth', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_all_user_by_auth_DBNoResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_all_user_by_auth', return_value=()):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_all_user_by_auth_DBResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_all_user_by_auth',
               return_value=(("date", "id", "name", "role"),)):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_banned_userid_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_banned_userid', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_banned_userid_DBNoResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_banned_userid', return_value=()):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_banned_userid_DBResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_banned_userid', return_value=(("id-1",),)):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_banstatus_by_id_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_banstatus_by_id', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_banstatus_by_id_DBNoResult():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_banstatus_by_id', return_value=()):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_banstatus_by_id_DBResultBan():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_banstatus_by_id', return_value=((0,),)):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_select_banstatus_by_id_DBResultNotBan():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.select_banstatus_by_id', return_value=((1,),)):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_update_user_accStatus_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.update_user_accStatus', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_update_user_accStatus_DBTrue():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.update_user_accStatus', return_value=True):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_update_user_accStatus_unban_DBError():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.update_user_accStatus_unban', return_value="some error"):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_update_user_accStatus_unban_DBTrue():
    with patch('Bluedit.admin.admin_gateway.AdminGateway.update_user_accStatus_unban', return_value=True):
        result = AdminManager()
        yield result


@pytest.fixture()
def mocked_insert_post_DBError():
    with patch('Bluedit.post.post_gateway.PostGateway.insert_post', return_value="some error"):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_insert_post_DBResult():
    with patch('Bluedit.post.post_gateway.PostGateway.insert_post', return_value=True):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_post_by_id_DBError():
    with patch('Bluedit.post.post_gateway.PostGateway.select_post_by_id', return_value="some error"):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_post_by_id_DBNoPost():
    with patch('Bluedit.post.post_gateway.PostGateway.select_post_by_id', return_value=[(), ()]):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_replies_by_postid_DBError():
    with patch('Bluedit.post.post_gateway.PostGateway.select_replies_by_postid', return_value="some error"):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_replies_by_postid_DBNoResult():
    with patch('Bluedit.post.post_gateway.PostGateway.select_replies_by_postid', return_value=()):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_insert_replies_DBError():
    with patch('Bluedit.post.post_gateway.PostGateway.insert_replies', return_value="some error"):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_insert_replies_DBResult():
    with patch('Bluedit.post.post_gateway.PostGateway.insert_replies', return_value=True):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_reply_by_replyid_DBError():
    with patch('Bluedit.post.post_gateway.PostGateway.select_reply_by_replyid', return_value="some error"):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_reply_by_replyid_DBNoResult():
    with patch('Bluedit.post.post_gateway.PostGateway.select_reply_by_replyid', return_value=()):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_update_reply_DBError():
    with patch('Bluedit.post.post_gateway.PostGateway.update_reply', return_value="some error"):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_update_reply_DBTrue():
    with patch('Bluedit.post.post_gateway.PostGateway.update_reply', return_value=True):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_exist_reply_by_id_DBError():
    with patch('Bluedit.post.post_gateway.PostGateway.select_exist_reply_by_id', return_value="some error"):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_exist_reply_by_id_DBExist():
    with patch('Bluedit.post.post_gateway.PostGateway.select_exist_reply_by_id', return_value=(0,)):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_exist_reply_reportuser_DBError():
    with patch('Bluedit.post.post_gateway.PostGateway.select_exist_reply_reportuser', return_value="some error"):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_exist_reply_reportuser_DBTrue():
    with patch('Bluedit.post.post_gateway.PostGateway.select_exist_reply_reportuser', return_value=(1,)):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_select_exist_reply_reportuser_DBFalse():
    with patch('Bluedit.post.post_gateway.PostGateway.select_exist_reply_reportuser', return_value=(0,)):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_insert_reportedreply_DBError():
    with patch('Bluedit.post.post_gateway.PostGateway.insert_reportedreply', return_value="some error"):
        result = PostManager()
        yield result


@pytest.fixture()
def mocked_insert_reportedreply_DBTrue():
    with patch('Bluedit.post.post_gateway.PostGateway.insert_reportedreply', return_value=True):
        result = PostManager()
        yield result
