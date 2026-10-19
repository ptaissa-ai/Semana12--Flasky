import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'apenas-desenvolvimento-altere-esta-chave')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_URL = os.environ.get('API_URL', 'https://api.sendgrid.com/v3/mail/send').strip()
    API_KEY = os.environ.get('API_KEY', '').strip()
    API_FROM = os.environ.get('API_FROM', '').strip()
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN', 'flaskaulasweb@zohomail.com').strip()
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flask] '
    STUDENT_ID = 'PT3038084'
    STUDENT_NAME = 'Taissa Pieri'
    STUDENT_EMAIL = 'p.taissa@aluno.ifsp.edu.br'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + str(BASE_DIR / 'instance' / 'app.db')

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(BASE_DIR / 'instance' / 'app.db')

config = {'development': DevelopmentConfig, 'testing': TestingConfig, 'production': ProductionConfig, 'default': DevelopmentConfig}
