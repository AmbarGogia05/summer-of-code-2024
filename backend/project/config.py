import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://admin:admin@localhost/db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False