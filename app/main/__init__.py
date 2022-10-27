from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from .config import environments
from datetime import timedelta

login_manager = LoginManager()
flask_bcrypt = Bcrypt()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.update(
        DEBUG=environments[config_name]["debug"],
        SECRET_KEY=environments[config_name]["secret_key"],
        SQLALCHEMY_DATABASE_URI=environments[config_name]["db"],
        SQLALCHEMY_TRACK_MODIFICATIONS="False",
        PERMANENT_SESSION_LIFETIME=timedelta(
            days=environments[config_name]["permanent_session_lifetime_days"]),
        SESSION_COOKIE_SECURE=environments[config_name]["session_cookie_secure"],
        SESSION_COOKIE_HTTPONLY=environments[config_name]["session_cookie_httponly"],
        # This would be if we chose to work with cookie duration after browser closure rather than "permanent" sessions
        # REMEMBER_COOKIE_DURATION=timedelta(minutes = environments[config_name]["remember_cookie_duration_minutes"]),
        # REMEMBER_COOKIE_SECURE=environments[config_name]["session_cookie_secure"],
        # REMEMBER_COOKIE_HTTPONLY=environments[config_name]["session_cookie_httponly"],

        # For debug
        # SQLALCHEMY_ECHO=True
    )
    CORS(
        app,
        resources={r"/*": {"origins": "*"}, r"/*/*": {"origins": "*"}, r"/*/*/*": {"origins": "*"}},
        automatic_options=False,
        methods=["GET", "POST", "PUT", "DELETE"],
        supports_credentials=True,
    )
    
    login_manager.init_app(app)
    flask_bcrypt.init_app(app)
    db.init_app(app)
    return app
