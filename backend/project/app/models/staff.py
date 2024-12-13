from . import db
from sqlalchemy import Column, String, Integer, Float, Boolean, Date, CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash
import re
import random
import string

class Staff(db.Model):
    __tablename__ = "Staff"

    s_ID = Column(String(15), primary_key=True)
    s_Name = Column(String(100), nullable=False)
    s_Email = Column(String(100), nullable=False, index=True)
    s_isAdmin = Column(Boolean, default=False)
    s_isActive = Column(Boolean, default=True)
    s_isApproved = Column(Boolean, default=True)
    s_Contact = Column(String(10), nullable=False)
    s_Password = Column("password", String(200), nullable=False)
    role = Column(String(10), default='staff', nullable=False)

    stafftransactions = db.relationship("Transaction", back_populates="staff")

    __table_args__ =(CheckConstraint("role IN ('staff')", name="check_role_values"),)
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the base constructor
        self.generate_id()  # Automatically generate a unique ID upon initialization

    def generate_id(self):
        while True:
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            new_id = f'STF-RND-{random_string}'
            # Check if the generated ID already exists
            if not Staff.query.filter_by(s_ID=new_id).first():
                self.s_ID = new_id
                break

    
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid Email Address")
        if Staff.query.filter_by(c_Email = email).first():
            raise ValueError("Email address already in use!")
    def validate_phone_number(contact):
        if not (isinstance(contact, str) and len(contact) == 10 and contact.isdigit()):
            raise ValueError(f"Invalid phone number: {contact}. It must be a string of exactly 10 digits.")
        if Staff.query.filter_by(c_Contact=contact).first():
            raise ValueError("Contact already in use!")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.s_isActive

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.s_ID)  # Ensure this returns a string

    @property   
    def password(self):
        raise AttributeError("Password is not readable")
    
    @password.setter
    def password(self, plain_password):
        self.s_Password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self.s_Password, plain_password)