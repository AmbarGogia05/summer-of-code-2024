from .init_db import db
from sqlalchemy import Column, String, Integer, Float, Boolean, Date #type: ignore
from sqlalchemy.exc import IntegrityError #type:ignore
import re
class InventoryItem(db.Model):
    __tablename__ = "InventoryItem"

    Item_SKU = db.Column(db.Integer, primary_key=True)
    Item_Name = db.Column(db.String(80), nullable=False)
    Item_Description = db.Column(db.String(200), nullable=True)
    Item_Price = db.Column(db.Float, nullable=False)
    Item_Qty = db.Column(db.Integer, nullable=False)

    def total_val(self):
        pricesandqty = InventoryItem.query.with_entities(InventoryItem.Item_Price, InventoryItem.Item_Qty).all()
        sum = 0
        return sum(price * qty for price, qty in pricesandqty)
    
    def validate_price(self):
        if self.Item_Price < 0:
            raise ValueError("Price must be non-negative")

class Customer(db.Model):
    __tablename__ = "Customer"

    c_ID = db.Column(db.Integer, primary_key=True)
    c_Name = db.Column(db.String(100), nullable=False)
    c_Email = db.Column(db.String(100), nullable=False, index=True)
    c_Contact = db.Column(db.String(10), nullable=False)

    def validate_email(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.c_Email):
            raise ValueError("Invalid Email Address")
    def validate_phone_number(self):
        if isinstance(self.c_Contact, str) and len(self.c_Contact) == 10 and self.c_Contact.isdigit():
            return True
        else:
            raise ValueError(f"Invalid phone number: {self.c_Contact}. It must be a string of exactly 10 digits.")


class Staff(db.Model):
    __tablename__ = "Staff"

    s_ID = db.Column(db.Integer, primary_key=True)
    s_Name = db.Column(db.String(100), nullable=False)
    s_Email = db.Column(db.String(100), nullable=False, index=True)
    s_isAdmin = db.Column(db.Boolean, nullable=False)
    s_Contact = db.Column(db.String(10), nullable=False)
    
    def validate_email(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.c_Email):
            raise ValueError("Invalid Email Address")
    def validate_phone_number(self):
        if isinstance(self.s_Contact, str) and len(self.s_Contact) == 10 and self.s_Contact.isdigit():
            return True
        else:
            raise ValueError(f"Invalid phone number: {self.s_Contact}. It must be a string of exactly 10 digits.")

class Transaction(db.Model):
    __tablename__ = "Transaction"

    t_ID = db.Column(db.Integer, primary_key=True)
    c_ID = db.Column(db.Integer, db.ForeignKey('Customer.c_ID'), nullable=False, index=True)
    t_Date = db.Column(db.Date, nullable=False)
    t_Amount = db.Column(db.Float, nullable=False)
    t_Category = db.Column(db.String(10), nullable=False)

    def validate_amount(self):
        if self.t_Amount < 0:
            raise ValueError("Total amount must be non-negative")
    def get_transactions(self, customer_id):
        return Transaction.query.filter_by(c_ID=customer_id).all()