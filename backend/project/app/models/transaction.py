from . import db
from sqlalchemy import Column, String, Integer, Float, Boolean, Date, Time, event, func
from sqlalchemy.exc import IntegrityError 
from sqlalchemy.dialects.postgresql import JSONB

class Transaction(db.Model):
    __tablename__ = "Transaction"

    t_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.String(15), db.ForeignKey('Customer.c_ID'), nullable=False)  # Customer ID
    s_id = db.Column(db.String(15), db.ForeignKey('Staff.s_ID'), nullable=False)  # Seller ID
    date = db.Column(db.Date, default = func.current_date(), nullable=False)
    time = db.Column(db.Time, default = func.current_time(), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    items = db.relationship("TransactionItem", back_populates="transaction")
    customer = db.relationship("Customer", back_populates="customertransactions")
    staff = db.relationship("Staff", back_populates="stafftransactions")
    
    def validate_amount(amount):
        if amount <= 0:
            raise ValueError("Total amount must be positive")
    
class TransactionItem(db.Model):
    __tablename__ = "TransactionItem"

    index = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('Transaction.t_id'), nullable=False)
    product_SKU = db.Column(db.Integer, db.ForeignKey('Product.Item_SKU'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    transaction = db.relationship("Transaction", back_populates="items")
    product = db.relationship("Product", back_populates="purchases")

class TransactionHistory(db.Model):
    __tablename__ = "TransactionHistory"
    index = db.Column(db.Integer, primary_key=True)
    t_id = db.Column(db.Integer, nullable=False)
    c_id = db.Column(db.String(15), nullable=False)  
    s_id = db.Column(db.String(15), nullable=False)  
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    items = db.Column(JSONB, nullable=False)

@event.listens_for(TransactionHistory, 'before_update')
def prevent_update(mapper, connection, target):
    raise Exception('Updates are not allowed on this table.')

@event.listens_for(TransactionHistory, 'before_delete')
def prevent_delete(mapper, connection, target):
    raise Exception('Deletes are not allowed on this table.')