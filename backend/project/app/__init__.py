from flask import Flask, render_template
from config import Config 
import psycopg2 
import os
from app.models import db, init_db
from flask_migrate import Migrate 
from app.api import api_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions here

    init_db(app) #initialize the db
    migrate = Migrate(app, db) #start migration
    
    # Register blueprints here
    app.register_blueprint(api_blueprint, url_prefix='/api')


    @app.route('/test/')
    def test_page():
        return render_template("product_add.html")
    
    @app.route('/clear_db')
    def clear():
        db.drop_all()
        db.create_all()
        return "DB CLEARED"
    return app