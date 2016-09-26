class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    SECRET_KEY = '\x1c\x07k5\xfc\x91{\x91x\xd2\\\x81el\xc3\x9d\xee\xed\xdeP\xa1\xda\xcd\xe0'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/dev_db.db'
    TESTING = True

class TestingConfig(Config):
    TESTING = True