from flaskext.mysql import MySQL
from flask_recaptcha import ReCaptcha
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

'''
Contains api singleton initialization.
--------------------------------------
Used by the app, this python file does not contain any scripts
'''
mysql = MySQL()
recaptcha = ReCaptcha()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()