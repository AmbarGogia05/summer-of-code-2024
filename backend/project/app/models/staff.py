from . import db
from sqlalchemy import Column, String, Integer, Float, Boolean, Date
from werkzeug.security import generate_password_hash, check_password_hash
import re

class Staff(db.Model):
    __tablename__ = "Staff"

    s_ID = Column(Integer, primary_key=True)
    s_Name = Column(String(100), nullable=False)
    s_Email = Column(String(100), nullable=False, index=True)
    s_isAdmin = Column(Boolean, nullable=False)
    s_Contact = Column(String(10), nullable=False)
    s_Password = Column("password", String(200), nullable=False)
    
    def validate_email(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.c_Email):
            raise ValueError("Invalid Email Address")
    
    def validate_phone_number(self):
        if isinstance(self.s_Contact, str) and len(self.s_Contact) == 10 and self.s_Contact.isdigit():
            return True
        else:
            raise ValueError(f"Invalid phone number: {self.s_Contact}. It must be a string of exactly 10 digits.")

    @property   
    def password(self):
        raise AttributeError("Password is not readable")
    
    @password.setter
    def password(self, plain_password):
        self.s_Password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self.s_Password, plain_password)