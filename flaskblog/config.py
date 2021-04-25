from os import environ


class Config():
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
