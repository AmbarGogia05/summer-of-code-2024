from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from app.models import db
from app.models.staff import Staff
from flask_login import login_user, logout_user, login_required, current_user
from flask_paginate import Pagination, get_page_args

staff_blueprint = Blueprint('staff', __name__)

@staff_blueprint.route('/login/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']

        member = Staff.query.filter_by(s_Email=email).first()

        if not member:
            flash('No such user!')
            return redirect(url_for('staff.login'))
        
        if member.check_password(password):
            login_user(member)  # Use Flask-Login to log the user in
            flash('Login successful')
            return redirect(url_for('staff.admin_home' if member.s_isAdmin else 'staff.staff_home'))  # yet to create admin_home and staff_home, do check

        else:
            flash('Incorrect email ID or password')
            return redirect(url_for('staff.login'))
        
    if request.method=='GET':
        if current_user.role == 'staff':
            if current_user.is_authenticated:
                flash('User already logged in')
                return redirect(url_for('staff.admin_home' if current_user.s_isAdmin else 'staff.staff_home'))
            else:
                return render_template('login.html')
        elif current_user.role =='customer':
            flash('Access Denied')
            return redirect(url_for('customer.home'))

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
                except ValueError:
                    flash('Invalid contact or email!')
                    return redirect(url_for('staff.add_staff'))
                
                new_member = Staff(s_Email=email, s_Name=name, s_Contact=contact, s_isAdmin=admin_status, s_isApproved=approval_status)

                new_member.password = password #hashes and stores

                db.session.add()
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
    
@staff_blueprint.route('/staff_home')
@login_required
def staff_home():
    if current_user.role == 'staff':
        return render_template('staff_home.html', user=current_user)
    else:
        flash('Access Denied')
        return redirect(url_for('customer.home'))

@staff_blueprint.route('/admin_home')
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

@staff_blueprint.route('/logout')
@login_required
def logout():
    if current_user.role =='staff':
        logout_user()
        flash('Logged out successfully!')
        return redirect(url_for('staff.login'))
    else:
        flash('Not staff member!')
        return redirect(url_for('customer.home'))
    
@staff_blueprint.route('/view_staff/', methods=['GET', 'POST'])
@login_required
def staff_view():
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