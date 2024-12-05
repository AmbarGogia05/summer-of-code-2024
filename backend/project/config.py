import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    DEBUG = os.getenv("DEBUG", False)
    TESTING = False

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", 5432),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

class DevelopmentConfig(Config):
    DEBUG = True
class ProductionConfig(Config):
    DEBUG = False

config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}