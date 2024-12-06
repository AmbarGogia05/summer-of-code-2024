from flask import Flask #type: ignore
from config import Config #type: ignore
import psycopg2 #type: ignore
import os
from .init_db import db, init_db
from flask_migrate import Migrate #type: ignore


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions here

    init_db(app) #initialize the db
    migrate = Migrate(app, db) #start migration
    
    # Register blueprints here


    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

