from flask import Flask, flash, redirect, url_for, session
from config import Config 
import psycopg2 
import os
from app.models import db, init_db
from app.models.customer import Customer
from app.models.staff import Staff
from flask_migrate import Migrate 
from app.main.product_blueprint import product_blueprint
from app.main.staff_blueprint import staff_blueprint
from app.main.customer_blueprint import customer_blueprint
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'dev'
    # Initialize Flask extensions here

    init_db(app) #initialize the db
    migrate = Migrate(app, db) #start migration
    
    # Register blueprints here
    app.register_blueprint(product_blueprint)
    app.register_blueprint(staff_blueprint, url_prefix='/staff/')
    app.register_blueprint(customer_blueprint)
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
    # Logic to load a user from your database
        if session['role'] == 'staff':
            return Staff.query.get(user_id)
        elif session['role'] == 'customer':
            return Customer.query.get(user_id)
        return None

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('You must be logged in to view this page.')
        return redirect(url_for('customer.login'))


    @app.route('/dev_reset/') #only for developmental stage, to be removed later
    def reset():
        db.drop_all()
        db.create_all()
        return "<h1>Database cleared</h1>"
    
    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

