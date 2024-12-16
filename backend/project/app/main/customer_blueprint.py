from flask import Blueprint, render_template, url_for, redirect, request, flash, session, make_response
from app.models import db
from app.models.customer import Customer
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, decode_token
from app.email_utils import send_verification_email, create_verification_token, create_reset_token, send_password_reset_email
import jwt
from config import Config
from functools import wraps
customer_blueprint = Blueprint('customer', __name__)

def logout_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            flash('Please logout to proceed!')
            if current_user.role == 'staff' and current_user.s_isAdmin == False:
                return redirect(url_for('staff.staff_home'))
            elif current_user.role == 'staff' and current_user.s_isAdmin:
                return redirect(url_for('staff.admin_home'))
            else:
                return redirect(url_for('customer.home'))
        return func(*args, **kwargs)
    return decorated_view


@customer_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        member = Customer.query.filter_by(c_Email=email).first()

        if not member:
            flash('No such user!')
            return redirect(url_for('customer.login'))
        
        if member.check_password(password):
            login_user(member)
            identity = member.c_ID  # Set `sub` as a string
            additional_claims = {
                "role": member.role,
            }
            
            access_token = create_access_token(identity=identity, additional_claims=additional_claims)

            response = make_response(redirect(url_for('customer.home')))

            set_access_cookies(response, access_token)
            print(f"User found: {member}, Active: {member.c_isActive}, Password check: {member.check_password(password)}")

            return response  # Return the response with the redirect and cookie
                            
        else:
            flash('Incorrect email ID or password')
            return redirect(url_for('customer.login'))
        
    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.role == 'staff' and not current_user.s_isAdmin:
                return redirect(url_for('staff.staff_home'))
            elif current_user.role =='staff' and current_user.s_isAdmin:
                return redirect(url_for('staff.admin_home'))
            else:
                return redirect(url_for('customer.home'))
        else:
            return render_template('login_customer.html')

@customer_blueprint.route('/logout/')
@login_required
def logout():
    if current_user.role == 'customer':
        logout_user()
        response = redirect(url_for('customer.login'))
        unset_jwt_cookies(response)
        flash('Logged out successfully!')
        return response
    else:
        flash('Not customer!')
        return redirect(url_for('staff.staff_home'))

@customer_blueprint.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        contact = request.form['contact']
        try:
            Customer.validate_email(email)
            Customer.validate_phone_number(contact)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('customer.signup'))
        
        new_member = Customer(c_Email=email, c_Name=name, c_Contact=contact)
        new_member.password = password  # Assuming this hashes and stores

        db.session.add(new_member)
        db.session.commit()
        flash('Account created successfully!')
        verification_token = create_verification_token(email)
        verification_link = f"http://127.0.0.1:5000/verify/{verification_token}"
        send_verification_email(email, verification_link)
        flash('Please verify your account through your registered email ID within 24 hours')
        return redirect(url_for("customer.login"))
    
    elif request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.role == 'staff':
                flash('Please log out to proceed!', 'error')
                return redirect(url_for('staff.staff_home' if not current_user.s_isAdmin else 'staff.admin_home'))
            else:
                flash('Account already logged in!')
                return redirect(url_for('customer.home'))
        return render_template('new_customer.html')

@customer_blueprint.route('/home/')
@login_required
def home():
    if current_user.role == 'customer':
        return render_template('customer_home.html')
    else:
        flash('Customer authentication needed!')
        if current_user.role == 'staff' and not current_user.s_isAdmin:
            return redirect(url_for('staff.staff_home'))
        else:
            return redirect(url_for('staff.admin_home'))

@customer_blueprint.route('/update_profile/', methods=['GET', 'POST'])
@login_required
def profile_update():
    if current_user.role == 'customer':
        if current_user.c_isActive:    
            if request.method == 'POST':
                email = request.form['email']
                name = request.form['name']
                contact = request.form['contact']

                if email and email != current_user.c_Email:
                    try:
                        Customer.validate_email(email)
                        current_user.c_Email = email
                    except ValueError as e:
                        flash(str(e), 'error')
                        return redirect(url_for('customer.profile_update'))
                
                if name:
                    current_user.c_Name = name
                
                if contact:
                    try:
                        Customer.validate_phone_number(contact)
                        current_user.c_Contact = contact
                    except ValueError as e:
                        flash(str(e), 'error')
                        return redirect(url_for('customer.profile_update'))
                    
                db.session.commit()
                flash('Profile updated!')
                return redirect(url_for('customer.profile_update'))
            elif request.method == 'GET':
                return render_template('update_profile.html', user=current_user)
        else:
            flash('Please activate your account by verifying your email address!')
            return redirect(url_for('customer.home'))
    else:
        flash('Not logged in as a customer!')
        return redirect(url_for('customer.login'))

@customer_blueprint.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        # Decode the token
        decoded = jwt.decode(token, Config.SENDGRID_API_KEY, algorithms=['HS256'])
        email = decoded['email']

        # Find the customer by email
        user = Customer.query.filter_by(c_Email=email).first()
        if user:
            user.c_isActive = True  # Mark user as active
            db.session.commit()
            flash("Your email has been verified!", "success")
            return redirect(url_for('customer.login'))
        else:
            flash("User not found.", "error")
    except jwt.ExpiredSignatureError:
        flash("The verification link has expired.", "error")
        return redirect(url_for('customer.login'))
    except jwt.InvalidTokenError:
        flash("Invalid verification link.", "error")
        return redirect(url_for('customer.login'))
    

@customer_blueprint.route('/password_reset/<token>', methods=['GET', 'POST'])
@logout_required
def reset_password(token):
    try:
        # Decode the token
        decoded = jwt.decode(token, Config.SENDGRID_API_KEY, algorithms=['HS256'])
        email = decoded['email']

        # Find the customer by email
        user = Customer.query.filter_by(c_Email=email).first()
        if request.method == 'POST':
            if user:
                user.password = request.form['new_password']
                db.session.commit()
                flash('Password has been reset')
                response = redirect(url_for('customer.login'))
                unset_jwt_cookies(response)
                return response
            else:
                flash("User not found.", "error")
                return redirect(url_for('customer.password_reset_request'))
        return render_template('customer_reset_password.html', token=token)
    except jwt.ExpiredSignatureError:
        flash("The reset link has expired.", "error")
        return redirect(url_for('customer.login'))
    except jwt.InvalidTokenError:
        flash("Invalid reset link.", "error")
        return redirect(url_for('customer.login'))
    
@customer_blueprint.route('/password_reset_request/', methods=['GET', 'POST'])
@logout_required
def password_reset_request():
    if request.method == 'POST':
        email = request.form['email']
        
        # Find the customer by email
        user = Customer.query.filter_by(c_Email=email).first()
        if user:
            # Create a token for the password reset link
            reset_token = create_reset_token(email)
            reset_link = f"http://127.0.0.1:5000/password_reset/{reset_token}"
            
            # Send the password reset email
            send_password_reset_email(email, reset_link)
            flash("A password reset link has been sent to your email address.", "success")
        else:
            flash("No account associated with that email address.", "error")
        
        return redirect(url_for('customer.password_reset_request'))

    return render_template('customer_password_reset_request.html')
