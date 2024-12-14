from flask import Flask, flash, redirect, url_for, session, jsonify
from config import Config 
from app.models import db, init_db
from app.models.customer import Customer
from app.models.staff import Staff
from flask_migrate import Migrate 
from app.main.product_blueprint import product_blueprint
from app.main.staff_blueprint import staff_blueprint
from app.main.customer_blueprint import customer_blueprint
from app.main.transaction_blueprint import transaction_blueprint
from flask_login import LoginManager
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'dev'

    init_db(app) #initialize the db
    migrate = Migrate(app, db) #start migration
    
    jwt = JWTManager(app)

    app.register_blueprint(product_blueprint)
    app.register_blueprint(staff_blueprint, url_prefix='/staff/')
    app.register_blueprint(customer_blueprint)
    app.register_blueprint(transaction_blueprint, url_prefix='/transactions/')
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
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
    
    @app.errorhandler(401)
    def unauthorized_error(e):
        return jsonify({"error": "Unauthorized access. Please login again."}), 401
    
    @app.errorhandler(403)
    def forbidden_error(e):
        return jsonify({"error": "You do not have permission to access this resource."}), 403
    
    @jwt.expired_token_loader
    def expired_token_callback(expired_token):
        return jsonify({"msg": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"msg": "Invalid token"}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"msg": "Missing token"}), 401
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500    
    
    return app

