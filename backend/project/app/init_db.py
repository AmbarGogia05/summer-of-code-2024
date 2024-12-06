from flask_sqlalchemy import SQLAlchemy #type: ignore
from .models import db

db = SQLAlchemy() #initialises database and creates tables that haven't already been created

def init_db(app):
    db.init_app(app) #binds db to the app instance
    with app.app_context():
        db.create_all()