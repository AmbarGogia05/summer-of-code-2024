from flask_sqlalchemy import SQLAlchemy #type: ignore

db = SQLAlchemy()

class InventoryItem(db.Model):
    __tablename__ = "InventoryItem"

    Item_SKU = db.Column(db.Integer, primary_key=True)
    Item_Name = db.Column(db.String(80), nullable=False)
    Item_Description = db.Column(db.String(200), nullable=False)
    Item_Price = db.Column(db.Float, nullable=False)
    Item_Qty = db.Column(db.Integer, nullable=False)

class Customer(db.Model):
    __tablename__ = "Customer"

    c_ID = db.Column(db.Integer, primary_key=True)
    c_Name = db.Column(db.String(100), nullable=False)
    c_Email = db.Column(db.String(100), nullable=False)
    c_Contact = db.Column(db.String(10), nullable=False)

class Staff(db.Model):
    __tablename__ = "Staff"

    s_ID = db.Column(db.Integer, primary_key=True)
    s_Name = db.Column(db.String(100), nullable=False)
    s_Email = db.Column(db.String(100), nullable=False)
    s_isAdmin = db.Column(db.Boolean, nullable=False)
    s_Contact = db.Column(db.String(10), nullable=False)
    
class Transaction(db.Model):
    __tablename__ = "Transaction"

    t_ID = db.Column(db.Integer, primary_key=True)
    c_ID = db.Column(db.Integer, db.ForeignKey('Customer.c_id'), nullable=False)
    t_Date = db.Column(db.Date, nullable=False)
    t_Amount = db.Column(db.Float, nullable=False)
    t_Category = db.Column(db.String(10), nullable=False)