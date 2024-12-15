import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://admin:admin@localhost/db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'dev'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_COOKIE_SECURE = False  # Set to True if using HTTPS
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_SENDER_EMAIL='posservicesproject@gmail.com'