from . import db
from sqlalchemy import Column, String, Integer, Float, Boolean, Date, CheckConstraint
import re
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(db.Model):
    __tablename__ = "Customer"

    c_ID = Column(String(15), primary_key=True)
    c_Name = Column(String(100), nullable=False)
    c_Email = Column(String(100), nullable=False, index=True)
    c_Contact = Column(String(10), nullable=False)
    c_Password = Column("password", String(200), nullable=False)
    role = Column(String(10), default='customer', nullable=False)
    c_isActive = Column(Boolean, default=False, nullable=False)


    customertransactions = db.relationship("Transaction", back_populates="customer")

    __table_args__ =(CheckConstraint("role IN ('customer')", name="check_role_values"),)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the base constructor
        if self.c_ID == None:
            self.generate_id()  # Automatically generate a unique ID upon initialization

    def generate_id(self):
        while True:
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            new_id = f'CTM-RND-{random_string}'
            # Check if the generated ID already exists
            if not Customer.query.filter_by(c_ID=new_id).first():
                self.c_ID = new_id
                break

    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid Email Address")
        if Customer.query.filter_by(c_Email = email).first():
            raise ValueError("Email address already in use!")
    def validate_phone_number(contact):
        if not (isinstance(contact, str) and len(contact) == 10 and contact.isdigit()):
            raise ValueError(f"Invalid phone number: {contact}. It must be a string of exactly 10 digits.")
        if Customer.query.filter_by(c_Contact=contact).first():
            raise ValueError("Contact already in use!")
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.c_isActive

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.c_ID)  # Ensure this returns a string

    @property   
    def password(self):
        raise AttributeError("Password is not readable")
    
    @password.setter
    def password(self, plain_password):
        self.c_Password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self.c_Password, plain_password)