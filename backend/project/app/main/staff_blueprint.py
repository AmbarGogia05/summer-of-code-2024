from flask import Blueprint, render_template, url_for, redirect, request, flash, session, make_response
from app.models import db
from app.models.staff import Staff
from app.models.customer import Customer
from flask_login import login_user, logout_user, login_required, current_user
from flask_paginate import Pagination, get_page_args
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from datetime import timedelta
import jwt
from config import Config
from app.email_utils import create_reset_token, send_password_reset_email
from functools import wraps
import pyotp
import qrcode
import secrets

staff_blueprint = Blueprint('staff', __name__)

def logout_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        flash('Please logout to proceed!')
        if current_user.is_authenticated:
            if current_user.role == 'staff' and current_user.s_isAdmin == False:
                return redirect(url_for('staff.staff_home'))
            elif current_user.role == 'staff' and current_user.s_isAdmin:
                return redirect(url_for('staff.admin_home'))
            else:
                return redirect(url_for('customer.home'))
        return func(*args, **kwargs)
    return decorated_view


@staff_blueprint.route('/login/', methods=['GET', 'POST'])
@logout_required
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        member = Staff.query.filter_by(s_Email=email).first()

        if not member:
            flash('No such user!')
            return redirect(url_for('staff.login'))
        
        if member.check_password(password):
            if member.is_2fa_enabled:
                token = secrets.token_hex(16)  
                session['2fa_token'] = token  
                session['s_ID'] = member.s_ID
                verification_url = url_for('staff.verify_2fa', _external=True, token=token)
                flash("Two-factor authentication required. Please check your authenticator app.")
                
                return redirect(verification_url)

            login_user(member)  
            flash('Login successful')
            access_token = create_access_token(identity=member.s_ID, 
                                                additional_claims={"role": member.role, "isadmin": member.s_isAdmin}, 
                                                expires_delta=timedelta(hours=1))
            
            response = make_response(redirect(url_for('staff.admin_home' if member.s_isAdmin else 'staff.staff_home')))
            set_access_cookies(response, access_token)
            return response
        else:
            flash('Incorrect email ID or password')
            return redirect(url_for('staff.login'))
        
    if request.method == 'GET':
        return render_template('login.html')
    
@staff_blueprint.route('/verify_2fa/<token>/', methods=['GET', 'POST'])
def verify_2fa(token):
    if '2fa_token' not in session or session['2fa_token'] != token:
        flash('Invalid or expired token!', 'error')
        return redirect(url_for('staff.login'))

    if request.method == 'POST':
        code = request.form['code']
        s_ID = session['s_ID']
        user = Staff.query.get(s_ID)
 
        if user.two_factor_secret:
            totp = pyotp.TOTP(user.two_factor_secret)
            if totp.verify(code):
                session.pop('2fa_token', None)
                session.pop('s_ID', None)
                login_user(user)
                flash("Two-factor authentication successful!")

                identity = user.s_ID
                additional_claims = {
                    "role": user.role,
                    "isadmin": user.s_isAdmin
                }
                
                access_token = create_access_token(identity=identity, additional_claims=additional_claims, expires_delta=timedelta(hours=1))
                response = make_response(redirect(url_for('staff.admin_home' if user.s_isAdmin else 'staff.staff_home')))
                set_access_cookies(response, access_token)

                return response 

            else:
                flash("Invalid code. Please try again.")

    return render_template('verify_2fa.html', token=token)

@staff_blueprint.route('/add-staff/', methods=['GET', 'POST'])
@login_required
def add_staff():
    if current_user.role == 'staff':
        if current_user.s_isAdmin:
            if request.method=='POST':
                email = request.form['email']
                password = request.form['password']
                name = request.form['name']
                contact = request.form['contact']
                admin_status = request.form['is_admin']
                approval_status = request.form['is_approved'] if not admin_status else 1 #admins given rights automatically
                try:
                    Staff.validate_email(email)
                    Staff.validate_phone_number(contact)
                except ValueError as e:
                    flash(str(e), 'error')
                    return redirect(url_for('staff.add_staff'))
                admin_status = int(admin_status)
                approval_status = int(approval_status)
                new_member = Staff(s_Email=email, s_Name=name, s_Contact=contact, s_isAdmin=admin_status, s_isApproved=approval_status)

                new_member.password = password #hashes and stores

                db.session.add(new_member)
                db.session.commit()
                flash('New member added to staff!')
                return redirect(url_for("staff.add_staff"))
            elif request.method=='GET':
                return render_template('create_user.html')

        else:
            flash('Admin permissions required!')
            return redirect(url_for('staff.staff_home'))
    else:
        flash('Access Denied')
        return redirect(url_for('customer.home'))
    
@staff_blueprint.route('/staff_home/')
@login_required
def staff_home():
    if current_user.role == 'staff' and not current_user.s_isAdmin:
        return render_template('staff_home.html', user=current_user)
    elif current_user.role == 'customer':
        flash('Access Denied')
        return redirect(url_for('customer.home'))
    else:
        return redirect(url_for('staff.admin_home'))

@staff_blueprint.route('/admin_home/')
@login_required
def admin_home():
    if current_user.role == 'staff':
        if current_user.s_isAdmin:
            return render_template('admin_home.html', user=current_user)
        else:
            flash('You do not have admin rights!')
            return redirect(url_for('staff.staff_home'))
    else:
        flash('Access Denied')
        return redirect(url_for('customer.home'))

@staff_blueprint.route('/logout/')
@login_required
def logout():
    if current_user.role =='staff':
        logout_user()
        response = redirect(url_for('staff.login'))
        unset_jwt_cookies(response)
        flash('Logged out successfully!')
        return response
    else:
        flash('Not staff member!')
        return redirect(url_for('customer.home'))
    
@staff_blueprint.route('/view_staff/', methods=['GET', 'POST'])
@login_required
def staff_view():
    if current_user.role == 'staff':
        page = request.args.get('page', 1, type=int)  # Current page number, gives default value 1
        per_page = 9  # Number of items per page

        if request.method=='POST':
            ID = request.form['ID']

            if ID:
                staff = Staff.query.get(ID)
                if staff:
                    staff_list = [staff]
                    return render_template('staff_query_result.html', staff_list = staff_list)
                else:
                    flash('No staff member with given ID')
                    return redirect(url_for('staff.staff_view'))
        
        if request.method=='GET':
            staff_query = Staff.query.all()
            total = len(staff_query)
            members = staff_query[(page - 1) * per_page: page * per_page]
            pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
            return render_template('view_staff.html', staff_list=members, pagination=pagination)
    else:
        flash('Not authorized!')
        return redirect(url_for('customer.login'))


@staff_blueprint.route('/view_customers/', methods=['GET', 'POST'])
@login_required
def customer_view():
    if current_user.role == 'staff':
        page = request.args.get('page', 1, type=int)  # Current page number, gives default value 1
        per_page = 9  # Number of items per page

        if request.method=='POST':
            ID = request.form['ID']

            if ID:
                customer = Customer.query.get(ID)
                if customer:
                    return render_template('customer_query_result.html', customer=customer)
                else:
                    flash('No customer with given ID')
                    return redirect(url_for('staff.customer_view'))
        
        if request.method=='GET':
            customer_query = Customer.query.all()
            total = len(customer_query)
            customers = customer_query[(page - 1) * per_page: page * per_page]
            pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
            return render_template('view_customers.html', customer_list=customers, pagination=pagination)
    else:
        flash('Not authorized!')
        return redirect(url_for('customer.login'))
    
@staff_blueprint.route('/update_staff/', methods=['GET', 'POST'])
@login_required
def update_staff():
    if current_user.role == 'staff' and current_user.s_isAdmin:
        if request.method=='POST':
            ID = request.form['ID']

            member = Staff.query.get(ID)

            if member:
                Name = request.form['name']
                Email = request.form['email']
                Contact = request.form['contact']
                isAdmin = request.form['admin']
                isActive = request.form['active']
                isApproved = request.form['approved']

                if Name:
                    member.s_Name = Name
                if Email:
                    try:
                        Staff.validate_email(Email)
                        member.s_Email = Email
                    except ValueError as e:
                        flash(str(e), 'error')
                        return redirect(url_for('staff.update_staff'))
                if Contact:
                    try:
                        Staff.validate_phone_number(Contact)
                        member.s_Contact = Contact
                    except ValueError as e:
                        flash(str(e), 'error')
                        return redirect(url_for('staff.update_staff'))
                if isAdmin:
                    isAdmin = int(isAdmin)
                    member.s_isAdmin = isAdmin
                if isActive:
                    isActive = int(isActive)
                    member.s_isActive = isActive
                if isApproved:
                    isApproved = int(isApproved)
                    member.s_isApproved = isApproved
                db.session.commit()
                flash('Update successful')
                return redirect(url_for('staff.update_staff'))
            else:
                flash('No such member of staff')
                return redirect(url_for('staff.update_staff'))
            
        if request.method=='GET':
            return render_template('update_staff.html')

    else:
        if current_user.role == 'staff' and not current_user.s_isAdmin:
            flash('You are not authorized to update staff!')
            return redirect(url_for('staff.staff_home'))
        else:
            flash('Not staff!')
            return redirect(url_for('customer.home'))

@staff_blueprint.route('/delete_staff/', methods=['GET', 'POST'])
@login_required
def delete_staff():
    if current_user.role == 'staff' and current_user.s_isAdmin:
        if request.method=='POST':
            ID = request.form['ID']
            if ID == 'STF-RND-000001':
                flash('User cannot be deleted!')
                return redirect(url_for('staff.delete_staff'))
            member = Staff.query.get(ID)
            if member:
                db.session.delete(member)
                db.session.commit()
                flash('Deleted member!')
                return redirect(url_for('staff.delete_staff'))
            else:
                flash('ID does not match!')
                return redirect(url_for('staff.delete_staff'))
        if request.method=='GET':
            return render_template('delete_staff.html')

    else:
        if current_user.role == 'staff' and not current_user.s_isAdmin:
            flash('You are not authorized to delete staff members!')
            return redirect(url_for('staff.staff_home'))
        else:
            flash('Not staff!')
            return redirect(url_for('customer.home'))
        
@staff_blueprint.route('/delete_customers/', methods=['GET', 'POST'])
@login_required
def delete_users():
    if current_user.role == 'staff' and current_user.s_isAdmin:
        if request.method=='POST':
            ID = request.form['ID']
            member = Customer.query.get(ID)
            if member:
                db.session.delete(member)
                db.session.commit()
                flash('Deleted member!')
                return redirect(url_for('staff.delete_users'))
            else:
                flash('ID does not match!')
                return redirect(url_for('staff.delete_users'))
        if request.method=='GET':
            return render_template('delete_users.html')

    else:
        if current_user.role == 'staff' and not current_user.s_isAdmin:
            flash('You are not authorized to delete customers!')
            return redirect(url_for('staff.staff_home'))
        else:
            flash('Not staff!')
            return redirect(url_for('customer.home'))
        
@staff_blueprint.route('/password_reset/<token>', methods=['GET', 'POST'])
@logout_required
def reset_password(token):
    try:
        # Decode the token
        decoded = jwt.decode(token, Config.SENDGRID_API_KEY, algorithms=['HS256'])
        email = decoded['email']

        user = Staff.query.filter_by(s_Email=email).first()
        if request.method == 'POST':
            if user:
                user.password = request.form['new_password']
                db.session.commit()
                flash('Password has been reset')
                response = redirect(url_for('staff.login'))
                unset_jwt_cookies(response)
                return response
            else:
                flash("User not found.", "error")
                return redirect(url_for('staff.password_reset_request'))
        return render_template('staff_reset_password.html', token=token)
    except jwt.ExpiredSignatureError:
        flash("The reset link has expired.", "error")
        return redirect(url_for('staff.login'))
    except jwt.InvalidTokenError:
        flash("Invalid reset link.", "error")
        return redirect(url_for('staff.login'))
    
@staff_blueprint.route('/password_reset_request/', methods=['GET', 'POST'])
@logout_required
def password_reset_request():
    if request.method == 'POST':
        email = request.form['email']
        
        user = Staff.query.filter_by(s_Email=email).first()
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

@staff_blueprint.route('/enable_2fa/', methods=['GET', 'POST'])
@login_required
def enable_2fa():
    user = current_user 
    if user.role == 'staff' and not user.is_2fa_enabled:
        if request.method == 'POST':
            # Generate a new TOTP secret
            user.two_factor_secret = pyotp.random_base32()
            db.session.commit()

            # Generate a QR code for the user
            totp = pyotp.TOTP(user.two_factor_secret)
            uri = totp.provisioning_uri(user.s_Email, issuer_name="PoSServices")
            img = qrcode.make(uri)
            img_path = f'static/qrcodes/{user.s_ID}.png'
            img.save(img_path)

            flash("Scan the QR code and enter a generated code to complete setup.")
            return render_template('enable_2fa.html', qr_code_url=img_path)  

        return render_template('enable_2fa.html')
    elif user.role == 'staff' and user.is_2fa_enabled:
        flash('Two-factor authentication is already enabled!')
        return redirect(url_for('staff.staff_home'))
    else:
        flash('Not staff!', 'error')
        return redirect(url_for('customer.home'))

@staff_blueprint.route('/verify_2fa_setup/', methods=['POST'])
@login_required
def verify_2fa_setup():
    user = current_user 
    code = request.form['otp']  
    if user.two_factor_secret:
        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(code):
            user.is_2fa_enabled = True
            db.session.commit()
            flash("Two-factor authentication setup successfully!")
            return redirect(url_for('staff.staff_home'))
        else:
            flash("Invalid code. Please try again.")

    return redirect(url_for('staff.enable_2fa'))
