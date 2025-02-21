import os

class Config:
    SECRET_KEY = os.environ.get('12IJ9NA9DJAS9D8JASD') or '12IJ9NA9DJAS9D8JASD'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'erp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False