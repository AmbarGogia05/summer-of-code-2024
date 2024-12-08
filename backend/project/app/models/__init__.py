from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy() #initialises database and creates tables that haven't already been created

from .customer import Customer
from .product import Product
from .staff import Staff
from .transaction import Transaction

def init_db(app):
    db.init_app(app) #binds db to the app instance
    with app.app_context():
        db.create_all()