from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import jwt
from datetime import datetime, timedelta
from config import Config

def create_verification_token(email):
    token = jwt.encode({
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=1)  
    }, Config.SENDGRID_API_KEY, algorithm='HS256') 
    return token

def send_verification_email(user_email, verification_link):
    message = Mail(
        from_email=current_app.config['SENDGRID_SENDER_EMAIL'],  
        to_emails=user_email,
        subject="Please verify your account",
        html_content=f"""
            <p>Thank you for registering!</p>
            <p>Please verify your email by clicking the link below:</p>
            <p><a href="{verification_link}">Verify Email</a></p>
        """
    )

    try:
        sg = SendGridAPIClient(current_app.config['SENDGRID_API_KEY'])  # Access the API key from the app config
        response = sg.send(message)
        print(f"Email sent to {user_email}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_reset_token(email):
    token = jwt.encode({
        'email': email,
        'exp': datetime.utcnow() + timedelta(minutes=15) 
    }, Config.SENDGRID_API_KEY, algorithm='HS256')  
    return token

def send_password_reset_email(user_email, reset_link):
    message = Mail(
        from_email=current_app.config['SENDGRID_SENDER_EMAIL'],
        to_emails=user_email,
        subject="Reset your password",
        html_content=f"""
        <p>Please ignore this email if you did not request a password reset.</p>
        <p>The link valid for 15 minutes to reset your password is below:</p>
        <p><a href="{reset_link}">Verify Email</a></p>
        """
    )

    try:
        sg = SendGridAPIClient(current_app.config['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(f"Password reset email sent to {user_email}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")