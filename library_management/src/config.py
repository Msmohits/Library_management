import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = False

    MARSHMALLOW_STRICT = True
    MARSHMALLOW_DATEFORMAT = 'rfc'

    SECRET_KEY = 'SECRETKEY@123'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(BaseConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    secret_key = 'test'


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    secret_key = 'test'


configs = {
    'dev': DevConfig,

    'default': DevConfig
}
