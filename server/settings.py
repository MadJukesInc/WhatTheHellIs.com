import tempfile
db_file = tempfile.NamedTemporaryFile()


class Config(object):
    SECRET_KEY = 'secret key'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    WTF_CSRF_ENABLED = False
    CACHE_TYPE = 'null'


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SERVER_URL = '0.0.0.0:1337'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    WTF_CSRF_ENABLED = False
    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True


class TestConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name
    SQLALCHEMY_ECHO = True

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
