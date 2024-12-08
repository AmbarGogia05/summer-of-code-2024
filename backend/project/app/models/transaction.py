from . import db
from sqlalchemy import Column, String, Integer, Float, Boolean, Date 
from sqlalchemy.exc import IntegrityError 

class Transaction(db.Model):
    __tablename__ = "Transaction"

    t_ID = Column(Integer, primary_key=True)
    c_ID = Column(Integer, db.ForeignKey('Customer.c_ID'), nullable=False, index=True)
    t_Date = Column(Date, nullable=False)
    t_Amount = Column(Float, nullable=False)
    t_Category = Column(String(10), nullable=False)

    def validate_amount(self):
        if self.t_Amount < 0:
            raise ValueError("Total amount must be non-negative")
    def get_transactions(self, customer_id):
        return Transaction.query.filter_by(c_ID=customer_id).all()