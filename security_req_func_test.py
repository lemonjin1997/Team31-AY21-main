import unittest
import datetime

from Bluedit import create_app
from config import TEST_CONFIG
from Bluedit.api import mysql


def clear_db():
    conn = mysql.connect()
    conn.commit()
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM user""")
    cursor.execute("""DELETE FROM post""")
    cursor.execute("""DELETE FROM post_blacklist""")
    cursor.execute("""DELETE FROM post_category""")
    cursor.execute("""DELETE FROM post_favourite""")
    cursor.execute("""DELETE FROM reply""")
    cursor.execute("""DELETE FROM reply_blacklist""")
    cursor.execute("""DELETE FROM reply_favourite""")
    cursor.execute("""DELETE FROM user_stash""")
    conn.commit()
    conn.close()


def insert_test_user(role):
    default_role = role
    f = '%Y-%m-%d %H:%M:%S'

    query_user = """INSERT INTO user VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    tuple_user = ("55165e12374011ec8be0ac1203ff3b87", "testemail@gmail.com",
                  "ed9fde443da702644c057aa15873b7787b9c1b9d92760502acabcf634d027fdb", "testonly", 1,
                  datetime.datetime.now().strftime(f), default_role, 1, 0, "2aF8jLWeBqoRZ0vU",
                  datetime.datetime.now().strftime(f))

    query_profile = """INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    tuple_profile = ("55165e12374011ec8be0ac1203ff3b87", "testuser", "test about", 0, 0, 0, 0, 0, "some image path")

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(query_user, tuple_user)
    cur.execute(query_profile, tuple_profile)
    conn.commit()
    conn.close()


def login(client, username, password):
    return client.post('/auth/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/auth/logout', follow_redirects=True)


class ReqTest(unittest.TestCase):
    def setUp(self):
        conf = TEST_CONFIG()
        app = create_app(conf)

        self.app = app.test_client()

    def tearDown(self):
        logout(self.app)
        clear_db()

    '''
    # Security Req 10:
    # The application shall authenticate the registered account by its email and password 
    # ----------------------------------------
    # Test case 1: Login test
    # Test case 2: Login + Logout test
    '''

    # Disabled CSRF, Email OTP, Email Verification for this test
    def test_login(self):
        insert_test_user("admin")
        rv = login(self.app, "testemail@gmail.com", "P@ssw0rd")
        assert rv.status_code == 200
        assert rv.request.path == "/"
        assert b'<a class="dropdown-item" href="/profile/user/testuser">My Profile</a>' in rv.data

    def test_logout(self):
        insert_test_user("admin")
        rv = login(self.app, "testemail@gmail.com", "P@ssw0rd")
        assert rv.request.path == "/"
        assert b'<a class="dropdown-item" href="/profile/user/testuser">My Profile</a>' in rv.data

        rv = logout(self.app)
        assert rv.request.path == "/"
        assert b'<a class="nav-link" href="/auth/login">Sign In</a>' in rv.data

    '''
    # Security Req 2:
    # The application shall not allow other users to view a user’s email address 
    # ----------------------------------------
    # Test case 1: Profile page get - assert email address do not exist
    # Test case 2: Profile manage get - assert email address do not exist
    # Test case 3: Admin user list get - assert email address do not exist
    # Test case 4: Home page get - assert email address do not exist
    '''

    def test_GETprofile_emailNotExist(self):
        insert_test_user("admin")
        login(self.app, "testemail@gmail.com", "P@ssw0rd")
        response = self.app.get('/profile/user/testuser', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/profile/user/testuser"
        assert b'class="btn btn-outline-dark btn-sm btn-block">Edit profile</a>' in response.data
        assert b'<h4 class="mt-0 mb-0">testuser</h4>' in response.data
        assert b'testemail@gmail.com' not in response.data

    def test_GETprofilemanage_emailNotExist(self):
        insert_test_user("admin")
        login(self.app, "testemail@gmail.com", "P@ssw0rd")
        response = self.app.get('/profile/management')
        assert response.status_code == 200
        assert response.request.path == "/profile/management"
        assert b'<small class="form-text text-muted">Note that you be logged out to re-verify your new email on' in response.data
        assert b'testemail@gmail.com' not in response.data

    def test_GETadmin_emailNotExist(self):
        insert_test_user("admin")
        login(self.app, "testemail@gmail.com", "P@ssw0rd")
        response = self.app.get('/admin')
        assert response.status_code == 200
        assert response.request.path == "/admin"
        assert b'testemail@gmail.com' not in response.data
        assert b'<h6>No existing users in the application</h6>' in response.data

    def test_GEThome_emailNotExist(self):
        insert_test_user("admin")
        login(self.app, "testemail@gmail.com", "P@ssw0rd")
        response = self.app.get('/')
        assert response.status_code == 200
        assert response.request.path == "/"
        assert b'testemail@gmail.com' not in response.data

    '''
    # Security Req 12
    # The application shall impose different privileges for different user roles  
    # -----------------------------
    # Test Case 1: Guest user try to manage profile - redirect to login
    # Test Case 2: Authenticated user try to manage profile - go to profile manage
    # Test Case 3: Authenticated user try to access admin page - go to home
    # Test Case 4: Admin user try to go admin page - go to admin page
    '''

    def test_GETprofilemanage_GuestUser(self):
        response = self.app.get('/profile/management', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/auth/login"
        assert b'Do not have an account ?' in response.data
        assert b'<a href="/auth/register">here</a> to sign up</p>' in response.data

    def test_GETprofilemanage_AuthUser(self):
        insert_test_user("user")
        login(self.app, "testemail@gmail.com", "P@ssw0rd")
        response = self.app.get('/profile/management', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/profile/management"
        assert b'<small class="form-text text-muted">Note that you be logged out to re-verify your new email on' in response.data
        assert b'testemail@gmail.com' not in response.data

    def test_GETadmin_AuthUser(self):
        insert_test_user("user")
        login(self.app, "testemail@gmail.com", "P@ssw0rd")
        response = self.app.get('/admin', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/"
        assert b'<label for="sort"><b>Sort By:</b></label>' in response.data

    def test_GETadmin_AdminUser(self):
        insert_test_user("admin")
        login(self.app, "testemail@gmail.com", "P@ssw0rd")
        response = self.app.get('/admin', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/admin"
        assert b'<h6>No existing users in the application</h6>' in response.data


if __name__ == '__main__':
    unittest.main()
