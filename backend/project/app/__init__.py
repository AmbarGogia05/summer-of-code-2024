from flask import Flask
from config import Config 
import psycopg2 
import os
from app.models import db, init_db
from flask_migrate import Migrate 
from app.main.product_blueprint import product_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'dev'

    # Initialize Flask extensions here

    init_db(app) #initialize the db
    migrate = Migrate(app, db) #start migration
    
    # Register blueprints here
    app.register_blueprint(product_blueprint)


    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

