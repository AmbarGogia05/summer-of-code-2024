from . import db
from sqlalchemy import Column, String, Integer, Float, Boolean, Date 
import re

class Customer(db.Model):
    __tablename__ = "Customer"

    c_ID = Column(Integer, primary_key=True)
    c_Name = Column(String(100), nullable=False)
    c_Email = Column(String(100), nullable=False, index=True)
    c_Contact = Column(String(10), nullable=False)

    def validate_email(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.c_Email):
            raise ValueError("Invalid Email Address")
    def validate_phone_number(self):
        if isinstance(self.c_Contact, str) and len(self.c_Contact) == 10 and self.c_Contact.isdigit():
            return True
        else:
            raise ValueError(f"Invalid phone number: {self.c_Contact}. It must be a string of exactly 10 digits.")
