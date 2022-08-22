from base64 import b64encode
import os

uri = os.environ.get("DATABASE_URL", "postgresql:///chessmate")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", b64encode(os.urandom(64)).decode("utf-8"))


class ProductionConfig(Config):
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = uri


class DevelopmentConfig(Config):
    ENV = "development"
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = uri


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "postgresql:///chessmate-test"
    DEBUG_TB_HOSTS = ["dont-show-debug-toolbar"]
    WTF_CSRF_ENABLED = False
