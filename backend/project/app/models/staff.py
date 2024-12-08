from . import db
from sqlalchemy import Column, String, Integer, Float, Boolean, Date 
import re

class Staff(db.Model):
    __tablename__ = "Staff"

    s_ID = Column(Integer, primary_key=True)
    s_Name = Column(String(100), nullable=False)
    s_Email = Column(String(100), nullable=False, index=True)
    s_isAdmin = Column(Boolean, nullable=False)
    s_Contact = Column(String(10), nullable=False)
    
    def validate_email(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.c_Email):
            raise ValueError("Invalid Email Address")
    def validate_phone_number(self):
        if isinstance(self.s_Contact, str) and len(self.s_Contact) == 10 and self.s_Contact.isdigit():
            return True
        else:
            raise ValueError(f"Invalid phone number: {self.s_Contact}. It must be a string of exactly 10 digits.")