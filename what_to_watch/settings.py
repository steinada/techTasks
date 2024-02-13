import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\stein\\PycharmProjects\\techTasks\\what_to_watch\\opinions_app\\db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    ENV = 'development'
    DEBUG = True
