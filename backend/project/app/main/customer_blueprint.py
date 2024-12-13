from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from app.models import db
from app.models.customer import Customer
from flask_login import login_user, logout_user, login_required, current_user

customer_blueprint = Blueprint('customer', __name__)

@customer_blueprint.route('/login/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']

        member = Customer.query.filter_by(c_Email=email).first()

        if not member:
            flash('No such user!')
            return redirect(url_for('customer.login'))
        
        if member.check_password(password):
            login_user(member)  # Use Flask-Login to log the user in
            flash('Login successful')
            return redirect(url_for('customer.home'))
                            
        else:
            flash('Incorrect email ID or password')
            return redirect(url_for('customer.login'))
        
    if request.method=='GET':
        if current_user.role == 'customer':
            if current_user.is_authenticated:
                flash('User already logged in')
                return redirect(url_for('customer.home'))
            else:
                return render_template('login_customer.html')

@customer_blueprint.route('/logout/')
@login_required
def logout():
    if current_user.role == 'customer':
        logout_user()
        flash('Logged out successfully!')
        return redirect(url_for('customer.login'))
    else:
        flash('Not customer!')
        return redirect(url_for('staff.staff_home'))
    
@customer_blueprint.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
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

        new_member.password = password #hashes and stores

        db.session.add()
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for("customer.home"))
    
    elif request.method=='GET':
        return render_template('create_user.html')

@customer_blueprint.route('/home/')
@login_required
def home():
    if current_user.role == 'customer' or (current_user.role == 'staff' and current_user.s_isAdmin):
        return render_template('customer_home.html')
    else:
        flash('Customer authentication needed!')
        if current_user.role == 'staff':
            return redirect(url_for('staff.staff_home'))

@customer_blueprint.route('/update_profile/', methods=['GET', 'POST'])
@login_required
def profile_update():
    if current_user.role == 'customer':
        if request.method == 'POST':
            email = request.form('email')
            name = request.form('name')
            contact = request.form('contact')

            if email:
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
            return render_template('update_profile.html', user = current_user)
    else:
        flash('Not logged in as a customer!')
        return redirect(url_for('customer.login'))
    
