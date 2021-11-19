# Importing open-source API(s)
from flask import Flask, session

# Importing required dependencies
from config import SQL_CONFIG
from Bluedit.api import mysql, recaptcha, mail, csrf, login_manager

# Importing Blueprints
from Bluedit.auth.auth_controller import auth_bp
from Bluedit.error.error_controller import error_bp
from Bluedit.home.home_controller import home_bp
from Bluedit.post.post_controller import post_bp
from Bluedit.profile.profile_controller import profile_bp
from Bluedit.admin.admin_controller import admin_bp


def create_app(config):
    # Flask Applet Initialization File
    app = Flask(__name__)

    # Getting configuration from config files
    app.config.from_object(config)

    # Adding those initialized singleton api into the applet
    mysql.init_app(app)
    recaptcha.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    login_manager.init_app(app)

    # Registering the blueprint to the applet
    app.register_blueprint(auth_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)

    # Management function to run before every request in the applet
    @app.before_request
    def session_management():
        session.modified = True

    return app


conf = SQL_CONFIG()
app = create_app(conf)

# Run the app
if __name__ == "__main__":
    app.run()
