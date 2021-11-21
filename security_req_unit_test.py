import pytest
from Bluedit.auth.models.AccountManager import AccountManager

'''
# Security Req 3
# The application shall clean the inputs before invoking the database 
# ------------------------------
# Unit test for all validation functions
'''


@pytest.fixture()
def username_input_valid():
    result = AccountManager().validate_input_NoSpecialCharacters("SomeValidUsername")
    return result


@pytest.fixture()
def username_input_invalid_TooLong():
    result = AccountManager().validate_input_NoSpecialCharacters("SomeValidUSomeValidUSomeValidUSomeValidUSomeValidU")
    return result


@pytest.fixture()
def username_input_invalid_Empty():
    result = AccountManager().validate_input_NoSpecialCharacters("")
    return result


@pytest.fixture()
def username_input_invalid_Special():
    result = AccountManager().validate_input_NoSpecialCharacters("S@meSp3c1@lN4m3!")
    return result


@pytest.fixture()
def username_input_invalid_Malicious():
    result = AccountManager().validate_input_NoSpecialCharacters("\';DROP sampletable;--")
    return result


@pytest.fixture()
def email_input_invalid_valid():
    result = AccountManager().validate_email_MatchFormat("someemail@gmail.com")
    return result


@pytest.fixture()
def email_input_invalid_invalid():
    result = AccountManager().validate_email_MatchFormat("someemailgmail.com")
    return result


@pytest.fixture()
def email_input_invalid_Malicious():
    result = AccountManager().validate_email_MatchFormat("\';DROP sampletable;--")
    return result


@pytest.fixture()
def content_input_validation():
    result = AccountManager().validate_text_replaceSymbol("hello world !!!!")
    return result


@pytest.fixture()
def content_input_validation_XSS():
    result = AccountManager().validate_text_replaceSymbol("<script>alert(1)</script>")
    return result


@pytest.fixture()
def content_input_validation_SQLI():
    result = AccountManager().validate_text_replaceSymbol("\';DROP sampletable;--")
    return result


def test_username_input_valid(username_input_valid):
    assert username_input_valid == True


def test_username_input_invalid_TooLong(username_input_invalid_TooLong):
    assert username_input_invalid_TooLong == False


def test_username_input_invalid_Empty(username_input_invalid_Empty):
    assert username_input_invalid_Empty == False


def test_username_input_invalid_Special(username_input_invalid_Special):
    assert username_input_invalid_Special == False


def test_username_input_invalid_Malicious(username_input_invalid_Malicious):
    assert username_input_invalid_Malicious == False


def test_email_input_invalid_valid(email_input_invalid_valid):
    assert email_input_invalid_valid == True


def test_email_input_invalid_invalid(email_input_invalid_invalid):
    assert email_input_invalid_invalid == False


def test_email_input_invalid_Malicious(email_input_invalid_Malicious):
    assert email_input_invalid_Malicious == False


def test_content_input_validation(content_input_validation):
    assert content_input_validation == "hello world &#33;&#33;&#33;&#33;"


def test_content_input_validation_XSS(content_input_validation_XSS):
    assert content_input_validation_XSS == "&#60;script&#62;alert&#40;1&#41;&#60;&#47;script&#62;"


def test_content_input_validation_SQLI(content_input_validation_SQLI):
    assert content_input_validation_SQLI == "&#39;&#59;DROP sampletable&#59;&#45;&#45;"


'''
# Security Req 4
# The application shall ensure the file is in the appropriate image format 
# --------------------------------------
# Unit test for file validation
'''


@pytest.fixture()
def filename_not_empty_setup():
    a = AccountManager().validate_filename_not_empty("somename.jpg")
    return a


@pytest.fixture()
def filename_empty_setup():
    a = AccountManager().validate_filename_not_empty("")
    return a


@pytest.fixture()
def filename_valid_setup():
    a = AccountManager().validate_filename_valid("somename.jpg")
    return a


@pytest.fixture()
def filename_invalid_setup():
    a = AccountManager().validate_filename_valid("notvalidfilename")
    return a


def test_filename_notempty(filename_not_empty_setup):
    assert filename_not_empty_setup == True


def test_filename_empty(filename_empty_setup):
    assert filename_empty_setup == False


def test_filename_valid(filename_valid_setup):
    assert filename_valid_setup == True


def test_filename_invalid(filename_invalid_setup):
    assert filename_invalid_setup == False


'''
# Security Req 8
# The application shall incorporate hash and salt algorithms to protect the account password 
# ---------------------------------------
# Unit test on hash algorithm
'''


@pytest.fixture()
def hash():
    hash_val = AccountManager().hash("hel10w0rld", ".r4t46sD")
    return hash_val


@pytest.fixture()
def hash_two():
    hash_one = AccountManager().hash("hel10w0rld", ".r4t46sD")
    hash_two = AccountManager().hash("hel10w0rld", "qQ4fbF21")
    return [hash_one, hash_two]


def test_hash_predetermineOutput(hash):
    assert hash == "c6e4e90dad8e7ab1b1b2c27e18e205ecb4410b9ab50b6fa46d2fdef185831251"


def test_hash_SamePasswordDifferentSalt(hash_two):
    hash_one = hash_two[0]
    hash_two = hash_two[1]
    assert hash_one != hash_two


'''
# Security Req 9
# The application shall implement a specific complexity criterion (at least 1 uppercase, 1 lower case and 1 number) for password when registering for accounts 
# ---------------------------------------
# Unit test on password validation
'''


@pytest.fixture()
def password_input_invalid_valid():
    result = AccountManager().validate_password_MatchFormat("t@stPassw0rd")
    return result


@pytest.fixture()
def password_input_invalid_invalid_TooShort():
    result = AccountManager().validate_password_MatchFormat("t@s.1t")
    return result


@pytest.fixture()
def password_input_invalid_invalid_NoSpecial():
    result = AccountManager().validate_password_MatchFormat("testpassword")
    return result


@pytest.fixture()
def password_input_invalid_invalid_NoUpper():
    result = AccountManager().validate_password_MatchFormat("@testpassword!")
    return result


@pytest.fixture()
def password_input_invalid_Malicious():
    result = AccountManager().validate_password_MatchFormat("\';DROP sampletable;--")
    return result


def test_password_input_invalid_valid(password_input_invalid_valid):
    assert password_input_invalid_valid == True


def test_password_input_invalid_invalid_TooShort(password_input_invalid_invalid_TooShort):
    assert password_input_invalid_invalid_TooShort == False


def test_password_input_invalid_invalid_NoSpecial(password_input_invalid_invalid_NoSpecial):
    assert password_input_invalid_invalid_NoSpecial == False


def test_password_input_invalid_invalid_NoUpper(password_input_invalid_invalid_NoUpper):
    assert password_input_invalid_invalid_NoUpper == False


def test_password_input_invalid_Malicious(password_input_invalid_Malicious):
    assert password_input_invalid_Malicious == False
