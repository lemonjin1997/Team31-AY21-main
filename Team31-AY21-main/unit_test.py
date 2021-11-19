from Bluedit.auth.models.Account import Account
from Bluedit.profile.models.Profile import Profile


def test_user_class(user):
    assert user.id == 123
    assert user.name == "test_name"
    assert user.role == "test_user"


def test_account_class(account):
    assert account.userID == "testid"
    assert account.email == "testemail"
    assert account.password == "testpassword"
    assert account.salt == "testsalt"
    assert account.dateCreated == "testdate"
    assert account.accStatus == 1
    assert account.activated == 1
    assert account.emailAuth == 1
    assert account.otpkey == "testkey"
    assert account.passwordDate == "test_pwdate"


def test_loaduser_idNone(mocked_load_user_dbwithresult):
    ans = mocked_load_user_dbwithresult.load_user(None)
    assert ans == None


def test_loaduser_dbresult(mocked_load_user_dbwithresult):
    ans = mocked_load_user_dbwithresult.load_user("someid")
    assert ans == (("some_result"),)


def test_loaduser_dberror(mocked_load_user_dberror):
    ans = mocked_load_user_dberror.load_user(id="someid")
    assert ans == -1


def test_generate_otpkey_DBError(mocked_select_exist_otpkey_error):
    ans = mocked_select_exist_otpkey_error.generate_otpkey()
    assert ans == -1


def test_generate_otpkey_DBPass(mocked_select_exist_otpkey_Pass):
    ans = mocked_select_exist_otpkey_Pass.generate_otpkey()
    assert ans != ""


def test_get_account_by_email_dbresult(mocked_get_account_by_email_dbresult):
    ans = mocked_get_account_by_email_dbresult.get_account_by_email("some_email")
    sample_acc = Account("testid", "testemail", "testpassword", "testsalt", "testdate", 1, 1, 1, "testkey",
                         "test_pwdate")
    assert ans.userID == sample_acc.userID
    assert ans.email == sample_acc.email
    assert ans.password == sample_acc.password
    assert ans.salt == sample_acc.salt
    assert ans.dateCreated == sample_acc.dateCreated
    assert ans.accStatus == sample_acc.accStatus
    assert ans.emailAuth == sample_acc.emailAuth
    assert ans.activated == sample_acc.activated
    assert ans.otpkey == sample_acc.otpkey
    assert ans.passwordDate == sample_acc.passwordDate


def test_get_account_by_email_dbnoresult(mocked_get_account_by_email_dbnoresult):
    ans = mocked_get_account_by_email_dbnoresult.get_account_by_email("some_email")
    assert ans == None


def test_get_account_by_email_dberror(mocked_get_account_by_email_dberror):
    ans = mocked_get_account_by_email_dberror.get_account_by_email("some_email")
    assert ans == -1


def test_check_activation_DBError(mocked_select_act_status_by_email_DBError):
    ans = mocked_select_act_status_by_email_DBError.check_activation("some_email")
    assert ans == -1


def test_check_activation_DBNoResult(mocked_select_act_status_by_email_DBNoResult):
    ans = mocked_select_act_status_by_email_DBNoResult.check_activation("some_email")
    assert ans == -2


def test_check_activation_DBActivated(mocked_select_act_status_by_email_DBActivated):
    ans = mocked_select_act_status_by_email_DBActivated.check_activation("some_email")
    assert ans == 1


def test_check_activation_DBNotActivated(mocked_select_act_status_by_email_DBNotActivated):
    ans = mocked_select_act_status_by_email_DBNotActivated.check_activation("some_email")
    assert ans == 0


def test_activate_account_DBError(mocked_update_act_status_by_email_DBError):
    ans = mocked_update_act_status_by_email_DBError.activate_account("some_email")
    assert ans == -1


def test_activate_account_DBPass(mocked_update_act_status_by_email_DBResult):
    ans = mocked_update_act_status_by_email_DBResult.activate_account("some_email")
    assert ans == ("some_value",)


def test_email_exist_DBError(mocked_email_exist_dberror):
    ans = mocked_email_exist_dberror.email_exist("someemail")
    assert ans == -1


def test_email_exist_DBTrue(mocked_email_exist_dbTrue):
    ans = mocked_email_exist_dbTrue.email_exist("someemail")
    assert ans == True


def test_email_exist_DBFalse(mocked_email_exist_dbFalse):
    ans = mocked_email_exist_dbFalse.email_exist("someemail")
    assert ans == False


def test_generate_salt_DBError(mocked_select_exist_salt_error):
    ans = mocked_select_exist_salt_error.generate_salt()
    assert ans == -1


def test_generate_salt_DBPass(mocked_select_exist_salt_Pass):
    ans = mocked_select_exist_salt_Pass.generate_salt()
    assert ans != ""


def test_update_password_DBError(mocked_update_password_by_email_DBError):
    ans = mocked_update_password_by_email_DBError.update_password("email", "password", "salt")
    assert ans == -1


def test_update_password_DBPass(mocked_update_password_by_email_DBResult):
    ans = mocked_update_password_by_email_DBResult.update_password("email", "password", "salt")
    assert ans == "some_value"


def test_username_exist_DBError(mocked_username_exist_dberror):
    ans = mocked_username_exist_dberror.username_exist("somename")
    assert ans == -1


def test_username_exist_DBTrue(mocked_username_exist_dbTrue):
    ans = mocked_username_exist_dbTrue.username_exist("somename")
    assert ans == True


def test_username_exist_DBFalse(mocked_username_exist_dbFalse):
    ans = mocked_username_exist_dbFalse.username_exist("somename")
    assert ans == False


def test_create_account_DBError(mocked_insert_new_user_DBError):
    ans = mocked_insert_new_user_DBError.create_account("salt", "otpkey", "email", "password", "username")
    assert ans == -1


def test_get_otp_key_DBError(mocked_select_otpkey_by_email_DBError):
    ans = mocked_select_otpkey_by_email_DBError.get_otp_key("some_email")
    assert ans == -1


def test_get_otp_key_DBNoResult(mocked_select_otpkey_by_email_DBNoResult):
    ans = mocked_select_otpkey_by_email_DBNoResult.get_otp_key("some_email")
    assert ans == False


def test_get_otp_key_DBResult(mocked_select_otpkey_by_email_DBResult):
    ans = mocked_select_otpkey_by_email_DBResult.get_otp_key("some_email")
    assert ans == "some_key"


def test_get_profile_DBError(mocked_select_profile_by_name_DBError):
    ans = mocked_select_profile_by_name_DBError.get_profile("some_name")
    assert ans == -1


def test_get_profile_DBNoResult(mocked_select_profile_by_name_DBNoResult):
    ans = mocked_select_profile_by_name_DBNoResult.get_profile("some_name")
    assert ans == -2


def test_get_profile_DBResult(mocked_select_profile_by_name_DBResult):
    ans = mocked_select_profile_by_name_DBResult.get_profile("some_name")
    profile = Profile("id", "name", "about", 0, 0, 0, 0, 0, "img")
    assert ans.userID == profile.userID
    assert ans.username == profile.username
    assert ans.about == profile.about
    assert ans.posted == profile.posted
    assert ans.commented == profile.commented
    assert ans.saved == profile.saved
    assert ans.reported == profile.reported
    assert ans.upvoted == profile.upvoted
    assert ans.profileImg == profile.profileImg


def test_get_user_post_top_3_DBError(mocked_select_top3user_post_by_name_DBError):
    ans = mocked_select_top3user_post_by_name_DBError.get_user_post_top_3("some name")
    assert ans == -1


def test_update_user_image_path_DBError(mocked_update_image_by_nameid_DBError):
    ans = mocked_update_image_by_nameid_DBError.update_user_image_path("path", "name", "id")
    assert ans == -1


def test_update_user_image_path_DBResult(mocked_update_image_by_nameid_DBTrue):
    ans = mocked_update_image_by_nameid_DBTrue.update_user_image_path("path", "name", "id")
    assert ans == True


def test_get_user_fa_status_DBError(mocked_select_fa_by_id_DBError):
    ans = mocked_select_fa_by_id_DBError.get_user_fa_status("some id")
    assert ans == -1


def test_get_user_fa_status_DBResult(mocked_select_fa_by_id_DBResult):
    ans = mocked_select_fa_by_id_DBResult.get_user_fa_status("some id")
    assert ans == 1


def test_update_username_DBError(mocked_update_name_by_nameid_DBError):
    ans = mocked_update_name_by_nameid_DBError.update_username("name", "name", "id")
    assert ans == -1


def test_update_username_DBTrue(mocked_update_name_by_nameid_DBTrue):
    ans = mocked_update_name_by_nameid_DBTrue.update_username("name", "name", "id")
    assert ans == True


def test_update_about_DBError(mocked_update_about_by_nameid_DBError):
    ans = mocked_update_about_by_nameid_DBError.update_about("name", "id", "about")
    assert ans == -1


def test_update_about_DBTrue(mocked_update_about_by_nameid_DBTrue):
    ans = mocked_update_about_by_nameid_DBTrue.update_about("name", "id", "about")
    assert ans == True


def test_authenticate_email_DBError(mocked_select_authenticate_email_DBError):
    ans = mocked_select_authenticate_email_DBError.authenticate_email("some_id", "some_email")
    assert ans == -1


def test_authenticate_email_DBTrue(mocked_select_authenticate_email_DBTrue):
    ans = mocked_select_authenticate_email_DBTrue.authenticate_email("some_id", "some_email")
    assert ans == True


def test_authenticate_email_DBFalse(mocked_select_authenticate_email_DBFalse):
    ans = mocked_select_authenticate_email_DBFalse.authenticate_email("some_id", "some_email")
    assert ans == False


def test_update_email_DBError(mocked_update_email_by_id_DBError):
    ans = mocked_update_email_by_id_DBError.update_email("some_email", "some_id")
    assert ans == -1


def test_update_email_DBPass(mocked_update_email_by_id_DBPass):
    ans = mocked_update_email_by_id_DBPass.update_email("some_email", "some_id")
    assert ans == True


def test_update_password_by_id_DBError(mocked_update_password_by_id_DBError):
    ans = mocked_update_password_by_id_DBError.update_password_by_id("id", "password", "salt")
    assert ans == -1


def test_update_password_by_id_DBPass(mocked_update_password_by_id_DBPass):
    ans = mocked_update_password_by_id_DBPass.update_password_by_id("id", "password", "salt")
    assert ans == True


def test_get_password_DBError(mocked_select_passwordsalt_by_id_DBError):
    ans = mocked_select_passwordsalt_by_id_DBError.get_password("some_id")
    assert ans == -1


def test_get_password_DBResult(mocked_select_passwordsalt_by_id_DBResult):
    ans = mocked_select_passwordsalt_by_id_DBResult.get_password("some_id")
    assert ans == ("some_result",)


def test_update_tfa_DBError(mocked_update_tfa_by_id_DBError):
    ans = mocked_update_tfa_by_id_DBError.update_tfa("some_id", "some_tfa_value")
    assert ans == -1


def test_update_tfa_DBPass(mocked_update_tfa_by_id_DBPass):
    ans = mocked_update_tfa_by_id_DBPass.update_tfa("some_id", "some_tfa_value")
    assert ans == True


def test_get_user_post_DBError(mocked_select_user_post_by_name_DBError):
    ans = mocked_select_user_post_by_name_DBError.get_user_post("some name")
    assert ans == -1


def test_get_stashed_post_DBError(mocked_select_stashed_post_by_id_DBError):
    ans = mocked_select_stashed_post_by_id_DBError.get_stashed_post("some id")
    assert ans == -1


def test_get_like_list_by_userid_DBError(mocked_select_like_by_userid_DBError):
    ans = mocked_select_like_by_userid_DBError.get_like_list_by_userid("some user id")
    assert ans == -1


def test_get_like_list_by_userid_DBNoResult(mocked_select_like_by_userid_DBNoResult):
    ans = mocked_select_like_by_userid_DBNoResult.get_like_list_by_userid("some user id")
    assert isinstance(ans, list) == True
    assert len(ans) == 0


def test_get_like_list_by_userid_DBResult(mocked_select_like_by_userid_DBResult):
    ans = mocked_select_like_by_userid_DBResult.get_like_list_by_userid("some user id")
    assert isinstance(ans, list) == True
    assert ("postid" in ans) == True


def test_get_save_list_by_userid_DBError(mocked_select_save_by_userid_DBError):
    ans = mocked_select_save_by_userid_DBError.get_save_list_by_userid("some user id")
    assert ans == -1


def test_get_save_list_by_userid_DBNoResult(mocked_select_save_by_userid_DBNoResult):
    ans = mocked_select_save_by_userid_DBNoResult.get_save_list_by_userid("some user id")
    assert isinstance(ans, list) == True
    assert len(ans) == 0


def test_get_save_list_by_userid_DBResult(mocked_select_save_by_userid_DBResult):
    ans = mocked_select_save_by_userid_DBResult.get_save_list_by_userid("some user id")
    assert isinstance(ans, list) == True
    assert ("postid" in ans) == True


def test_get_upvote_post_DBError(mocked_select_upvote_post_by_id_DBError):
    ans = mocked_select_upvote_post_by_id_DBError.get_upvote_post("some id")
    assert ans == -1


def test_get_upvote_reply_DBError(mocked_select_upvoted_reply_by_id_DBError):
    ans = mocked_select_upvoted_reply_by_id_DBError.get_upvote_reply("some id")
    assert ans == -1


def test_get_r_like_list_by_userid_DBError(mocked_select_r_like_by_userid_DBError):
    ans = mocked_select_r_like_by_userid_DBError.get_r_like_list_by_userid("some user id")
    assert ans == -1


def test_get_r_like_list_by_userid_DBNoResult(mocked_select_r_like_by_userid_DBNoResult):
    ans = mocked_select_r_like_by_userid_DBNoResult.get_r_like_list_by_userid("some user id")
    assert isinstance(ans, list) == True
    assert len(ans) == 0


def test_get_r_like_list_by_userid_DBResult(mocked_select_r_like_by_userid_DBResult):
    ans = mocked_select_r_like_by_userid_DBResult.get_r_like_list_by_userid("some user id")
    assert isinstance(ans, list) == True
    assert ("replyid" in ans) == True


def test_get_commented_post_DBError(mocked_select_commented_post_by_id_DBError):
    ans = mocked_select_commented_post_by_id_DBError.get_commented_post("some id")
    assert ans == -1


def test_get_commented_post_DBResult(mocked_select_commented_post_by_id_DBResult):
    ans = mocked_select_commented_post_by_id_DBResult.get_commented_post("some id")
    assert isinstance(ans, list) == True


def test_get_commented_post_DBNoResult(mocked_select_commented_post_by_id_DBNoResult):
    ans = mocked_select_commented_post_by_id_DBNoResult.get_commented_post("some id")
    assert isinstance(ans, list) == True
    assert len(ans) == 0


def test_search_postTitle_DBError(mocked_get_all_post_with_conditions_DBError):
    ans = mocked_get_all_post_with_conditions_DBError.search_postTitle("target", "value")
    assert ans == -1


def test_search_postContent_DBError(mocked_get_all_post_with_conditions_DBError):
    ans = mocked_get_all_post_with_conditions_DBError.search_postContent("target", "value")
    assert ans == -1


def test_search_UUID_DBError(mocked_get_all_post_with_conditions_DBError):
    ans = mocked_get_all_post_with_conditions_DBError.search_UUID("value")
    assert ans == -1


def test_search_postCat_DBError(mocked_get_all_post_DBError):
    ans = mocked_get_all_post_DBError.search_postCat("value")
    assert ans == -1


def test_get_all_post_DBError(mocked_get_all_post_home_DBError):
    ans = mocked_get_all_post_home_DBError.get_all_post()
    assert ans == -1


def test_get_user_DBError(mocked_select_all_user_DBError):
    ans = mocked_select_all_user_DBError.get_user()
    assert ans == -1


def test_get_user_DBNoResult(mocked_select_all_user_DBNoResult):
    ans = mocked_select_all_user_DBNoResult.get_user()
    assert ans == False


def test_get_user_DBResult(mocked_select_all_user_DBResult):
    ans = mocked_select_all_user_DBResult.get_user()
    assert isinstance(ans, tuple) == True


def test_promote_user_DBError(mocked_update_userrole_by_id_DBError):
    ans = mocked_update_userrole_by_id_DBError.promote_user("id")
    assert ans == -1


def test_promote_user_DBTrue(mocked_update_userrole_by_id_DBTrue):
    ans = mocked_update_userrole_by_id_DBTrue.promote_user("id")
    assert ans == True


def test_get_reported_post_DBError(mocked_select_reported_post_list_DBError):
    ans = mocked_select_reported_post_list_DBError.get_reported_post()
    assert ans == -1


def test_get_reported_post_DBNoResult(mocked_select_reported_post_list_DBNoResult):
    ans = mocked_select_reported_post_list_DBNoResult.get_reported_post()
    assert ans == False


def test_get_reported_post_DBResult(mocked_select_reported_post_list_DBResult):
    ans = mocked_select_reported_post_list_DBResult.get_reported_post()
    assert isinstance(ans, list) == True


def test_get_locked_post_DBError(mocked_select_locked_post_DBError):
    ans = mocked_select_locked_post_DBError.get_locked_post()
    assert ans == -1


def test_get_locked_post_DBNoResult(mocked_select_locked_post_DBNoResult):
    ans = mocked_select_locked_post_DBNoResult.get_locked_post()
    assert ans == False


def test_get_locked_post_DBResult(mocked_select_locked_post_DBResult):
    ans = mocked_select_locked_post_DBResult.get_locked_post()
    assert isinstance(ans, tuple) == True


def test_check_post_lock_status_DBError(mocked_select_lockstatus_by_id_DBError):
    ans = mocked_select_lockstatus_by_id_DBError.check_post_lock_status("id")
    assert ans == -1


def test_check_post_lock_status_DBNoResult(mocked_select_lockstatus_by_id_DBNoResult):
    ans = mocked_select_lockstatus_by_id_DBNoResult.check_post_lock_status("id")
    assert ans == -2


def test_check_post_lock_status_DBResultLock(mocked_select_lockstatus_by_id_DBResultLock):
    ans = mocked_select_lockstatus_by_id_DBResultLock.check_post_lock_status("id")
    assert ans == True


def test_check_post_lock_status_DBResultUnlock(mocked_select_lockstatus_by_id_DBResultUnlock):
    ans = mocked_select_lockstatus_by_id_DBResultUnlock.check_post_lock_status("id")
    assert ans == False


def test_lock_post_DBError(mocked_update_postlock_DBError):
    ans = mocked_update_postlock_DBError.lock_post("id")
    assert ans == -1


def test_lock_post_DBTrue(mocked_update_postlock_DBTrue):
    ans = mocked_update_postlock_DBTrue.lock_post("id")
    assert ans == True


def test_unlock_post_DBError(mocked_update_postlock_unlock_DBError):
    ans = mocked_update_postlock_unlock_DBError.unlock_post("id")
    assert ans == -1


def test_unlock_post_DBTrue(mocked_update_postlock_unlock_DBTrue):
    ans = mocked_update_postlock_unlock_DBTrue.unlock_post("id")
    assert ans == True


def test_get_reported_reply_DBError(mocked_select_reported_reply_list_DBError):
    ans = mocked_select_reported_reply_list_DBError.get_reported_reply()
    assert ans == -1


def test_get_reported_reply_DBNoResult(mocked_select_reported_reply_list_DBNoResult):
    ans = mocked_select_reported_reply_list_DBNoResult.get_reported_reply()
    assert ans == False


def test_get_reported_reply_DBResult(mocked_select_reported_reply_list_DBResult):
    ans = mocked_select_reported_reply_list_DBResult.get_reported_reply()
    assert ans[0][0] == "id"


def test_get_all_user_DBError(mocked_select_all_user_by_auth_DBError):
    ans = mocked_select_all_user_by_auth_DBError.get_all_user()
    assert ans == -1


def test_get_all_user_DBNoResult(mocked_select_all_user_by_auth_DBNoResult):
    ans = mocked_select_all_user_by_auth_DBNoResult.get_all_user()
    assert ans == False


def test_get_all_user_DBResult(mocked_select_all_user_by_auth_DBResult):
    ans = mocked_select_all_user_by_auth_DBResult.get_all_user()
    assert ans[0][0] == "date"


def test_get_ban_list_DBError(mocked_select_banned_userid_DBError):
    ans = mocked_select_banned_userid_DBError.get_ban_list()
    assert ans == -1


def test_get_ban_list_DBNoResult(mocked_select_banned_userid_DBNoResult):
    ans = mocked_select_banned_userid_DBNoResult.get_ban_list()
    assert ans == False


def test_get_ban_list_DBResult(mocked_select_banned_userid_DBResult):
    ans = mocked_select_banned_userid_DBResult.get_ban_list()
    assert ans[0][0] == "id-1"


def test_check_ban_status_DBError(mocked_select_banstatus_by_id_DBError):
    ans = mocked_select_banstatus_by_id_DBError.check_ban_status("id")
    assert ans == -1


def test_check_ban_status_DBNoResult(mocked_select_banstatus_by_id_DBNoResult):
    ans = mocked_select_banstatus_by_id_DBNoResult.check_ban_status("id")
    assert ans == -2


def test_check_ban_status_DBResultBan(mocked_select_banstatus_by_id_DBResultBan):
    ans = mocked_select_banstatus_by_id_DBResultBan.check_ban_status("id")
    assert ans == True


def test_check_ban_status_DBResultNotBan(mocked_select_banstatus_by_id_DBResultNotBan):
    ans = mocked_select_banstatus_by_id_DBResultNotBan.check_ban_status("id")
    assert ans == False


def test_ban_user_DBError(mocked_update_user_accStatus_DBError):
    ans = mocked_update_user_accStatus_DBError.ban_user("id")
    assert ans == -1


def test_ban_user_DBTrue(mocked_update_user_accStatus_DBTrue):
    ans = mocked_update_user_accStatus_DBTrue.ban_user("id")
    assert ans == True


def test_unban_user_DBError(mocked_update_user_accStatus_unban_DBError):
    ans = mocked_update_user_accStatus_unban_DBError.unban_user("id")
    assert ans == -1


def test_unban_user_DBTrue(mocked_update_user_accStatus_unban_DBTrue):
    ans = mocked_update_user_accStatus_unban_DBTrue.unban_user("id")
    assert ans == True


def test_upload_post_DBError(mocked_insert_post_DBError):
    ans = mocked_insert_post_DBError.upload_post("title", "content", "cat", "path", "id")
    assert ans == -1


def test_upload_post_DBResult(mocked_insert_post_DBResult):
    ans = mocked_insert_post_DBResult.upload_post("title", "content", "cat", "path", "id")
    assert len(ans) == 32


def test_get_post_DBError(mocked_select_post_by_id_DBError):
    ans = mocked_select_post_by_id_DBError.get_post("id")
    assert ans == -1


def test_get_post_DBNoPost(mocked_select_post_by_id_DBNoPost):
    ans = mocked_select_post_by_id_DBNoPost.get_post("id")
    assert ans == -2


def test_get_replies_DBError(mocked_select_replies_by_postid_DBError):
    ans = mocked_select_replies_by_postid_DBError.get_replies("id")
    assert ans == -1


def test_get_replies_DBNoResult(mocked_select_replies_by_postid_DBNoResult):
    ans = mocked_select_replies_by_postid_DBNoResult.get_replies("id")
    assert ans == -2


def test_upload_comments_DBError(mocked_insert_replies_DBError):
    ans = mocked_insert_replies_DBError.upload_comments("postid", 'userid', "comment")
    assert ans == -1


def test_upload_comments_DBResult(mocked_insert_replies_DBResult):
    ans = mocked_insert_replies_DBResult.upload_comments("postid", 'userid', "comment")
    assert len(ans) == 32


def test_get_reply_by_replyid_DBError(mocked_select_reply_by_replyid_DBError):
    ans = mocked_select_reply_by_replyid_DBError.get_reply_by_replyid("id")
    assert ans == -1


def test_get_reply_by_replyid_DBNoResult(mocked_select_reply_by_replyid_DBNoResult):
    ans = mocked_select_reply_by_replyid_DBNoResult.get_reply_by_replyid("id")
    assert ans == -2


def test_update_reply_DBError(mocked_update_reply_DBError):
    ans = mocked_update_reply_DBError.update_reply("id", "content")
    assert ans == -1


def test_update_reply_DBTrue(mocked_update_reply_DBTrue):
    ans = mocked_update_reply_DBTrue.update_reply("id", "content")
    assert ans == True


def test_check_reply_exist_DBError(mocked_select_exist_reply_by_id_DBError):
    ans = mocked_select_exist_reply_by_id_DBError.check_reply_exist("id")
    assert ans == -1


def test_check_reply_exist_DBExist(mocked_select_exist_reply_by_id_DBExist):
    ans = mocked_select_exist_reply_by_id_DBExist.check_reply_exist("id")
    assert ans == 0


def test_check_reply_report_list_DBError(mocked_select_exist_reply_reportuser_DBError):
    ans = mocked_select_exist_reply_reportuser_DBError.check_reply_report_list("replyid", "userid")
    assert ans == -1


def test_check_reply_report_list_DBTrue(mocked_select_exist_reply_reportuser_DBTrue):
    ans = mocked_select_exist_reply_reportuser_DBTrue.check_reply_report_list("replyid", "userid")
    assert ans == True


def test_check_reply_report_list_DBFalse(mocked_select_exist_reply_reportuser_DBFalse):
    ans = mocked_select_exist_reply_reportuser_DBFalse.check_reply_report_list("replyid", "userid")
    assert ans == False


def test_report_reply_DBError(mocked_insert_reportedreply_DBError):
    ans = mocked_insert_reportedreply_DBError.report_reply("replyid", "userid")
    assert ans == -1


def test_report_reply_DBTrue(mocked_insert_reportedreply_DBTrue):
    ans = mocked_insert_reportedreply_DBTrue.report_reply("replyid", "userid")
    assert ans == True


