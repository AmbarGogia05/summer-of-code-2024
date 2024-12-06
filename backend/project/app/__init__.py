from flask import Flask #type: ignore
from config import config_map, DB_CONFIG #type: ignore
import psycopg2 #type: ignore
import os

def create_app():
    app = Flask(__name__)
    config_name = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_map[config_name])

    # Initialize Flask extensions here

    # Register blueprints here

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

def get_db_connection(host, port, dbname, user, password):
    host = DB_CONFIG["host"]
    port = DB_CONFIG["port"]
    dbname = DB_CONFIG["dbname"]
    user = DB_CONFIG["user"]
    password = DB_CONFIG["password"]

    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )

    return connection