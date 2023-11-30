import os

postgres_data_base = os.getenv("PGSTRING")
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://stock:jwt78IF&33G=@localhost/stock'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config_by_name = dict(dev=DevelopmentConfig, prod=ProductionConfig)

key = Config.SECRET_KEY
