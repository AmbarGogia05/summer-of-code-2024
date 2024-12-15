from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from app.models import db
from app.models.product import Product
from flask_login import login_user, logout_user, login_required, current_user
from flask_paginate import Pagination, get_page_args

product_blueprint = Blueprint('product', __name__)

@product_blueprint.route('/create/', methods=['GET','POST'])
@login_required
def create_product():  # to create a new product
    if current_user.role == 'staff' and current_user.s_isApproved:
        if request.method == 'POST':
            name = request.form['name']
            desc = request.form['desc']
            price = request.form['price']
            qty = request.form['qty']

            if not name or not price or not qty:
                flash('All fields are required!', 'error')
                return redirect(url_for('product.create_product'))

            try:
                price = float(price)
                qty = int(qty)
                new_prod = Product(Item_Name=name, Item_Description=desc, Item_Price=price, Item_Qty=qty)
                new_prod.validate_price_and_qty()  # Assuming this method raises exceptions as needed

                db.session.add(new_prod)
                db.session.commit()
                session['new_prod_id'] = new_prod.Item_SKU
                flash('Product added successfully', 'success')
            except ValueError as e:
                flash(str(e), 'error')
            except Exception as e:  # Handle any database-related errors
                flash('An error occurred while adding the product: ' + str(e), 'error')
            return redirect(url_for('product.create_product'))

        # Handle GET request
        product = None
        if 'new_prod_id' in session:
            prod_id = session.pop('new_prod_id')
            product = Product.query.get(prod_id)
        return render_template('create_product.html', product=product)

    if current_user.role == 'staff' and not current_user.s_isApproved:
        flash('You are not authorized to add products!')
        return redirect(url_for('staff.staff_home'))

    flash('Not staff!')
    return redirect(url_for('customer.home'))

@product_blueprint.route('/delete/', methods=['GET', 'POST'])
@login_required
def delete_product():
    if current_user.role == 'staff' and current_user.s_isApproved:
        if request.method == 'POST':
            sku = request.form['sku']
            prod = Product.query.get(sku)

            if prod:
                db.session.delete(prod)
                try:
                    db.session.commit()
                    flash('Product deleted successfully', 'success')
                except Exception as e:
                    flash('An error occurred while deleting the product: ' + str(e), 'error')
            else:
                flash('No such item')

            return redirect(url_for('product.delete_product'))

        # Handle GET request
        return render_template('delete_product.html')

    if current_user.role == 'staff' and not current_user.s_isApproved:
        flash('You are not authorized to delete products!')
        return redirect(url_for('staff.staff_home'))

    flash('Not staff!')
    return redirect(url_for('customer.home'))

@product_blueprint.route('/update/', methods=['GET', 'POST'])
@login_required
def update_product():
    if current_user.role == 'staff' and current_user.s_isApproved:
        if request.method == 'POST':
            sku = request.form['sku']
            prod = Product.query.get(sku)

            if prod:
                name = request.form['name']
                desc = request.form['desc']
                price = request.form['price']
                qty = request.form['qty']

                if name:
                    prod.Item_Name = name
                if desc:
                    prod.Item_Description = desc

                try:
                    if price:
                        prod.Item_Price = float(price)
                    if qty:
                        prod.Item_Qty = int(qty)
                    prod.validate_price_and_qty()  # Assuming this method raises exceptions as needed

                    db.session.commit()
                    flash('Update successful', 'success')
                except ValueError as e:
                    flash(str(e), 'error')
                except Exception as e:  # Handle any database-related errors
                    flash('An error occurred while updating the product: ' + str(e), 'error')
                session['prod_id'] = sku
                return redirect(url_for('product.update_product'))
            else:
                flash('No such product')
                return redirect(url_for('product.update_product'))

        # Handle GET request
        prod = None
        if 'prod_id' in session:
            id = session.pop('prod_id')
            prod = Product.query.get(id)
        return render_template('update_product.html', product=prod)

    if current_user.role == 'staff' and not current_user.s_isApproved:
        flash('You are not authorized to update products!')
        return redirect(url_for('staff.staff_home'))

    flash('Not staff!')
    return redirect(url_for('customer.home'))

@product_blueprint.route('/view/', methods=['GET', 'POST'])
def product_view():
    page = request.args.get('page', 1, type=int)  # Current page number, gives default value 1
    per_page = 9  # Number of items per page

    if request.method == 'POST':
        sku = request.form['sku']
        name = request.form['name']
        sort_by = request.form.getlist('sort_by')  # Get sorting options

        if sku and not name:
            prod = Product.query.get(sku)
            if prod:
                prod_list = [prod]
                return render_template('query_result.html', prod_list=prod_list)
            else:
                flash('No such product')
                return redirect(url_for('product.product_view'))

        elif name and not sku:
            prod_list = Product.query.filter_by(Item_Name=name).all()
            if prod_list:
                if sort_by:  # Sort based on user selection
                    prod_list = sorted(prod_list, key=lambda x: tuple(getattr(x, param) for param in sort_by))
                total = len(prod_list)
                products = prod_list[(page - 1) * per_page: page * per_page]
                pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
                return render_template('query_result.html', prod_list=products, pagination=pagination)
            else:
                flash('No such product')
                return redirect(url_for('product.product_view'))

        elif name and sku:
            prod_list = Product.query.filter_by(Item_SKU=sku, Item_Name=name).all()
            if prod_list:  # Sorting not necessary, searching by sku gives just one output
                return render_template('query_result.html', prod_list=prod_list)
            else:
                flash('No such product')
                return redirect(url_for('product.product_view'))

        else:
            prod_list = Product.query.all()
            if prod_list:
                if sort_by:  # Sort based on user selection
                    prod_list = sorted(prod_list, key=lambda x: tuple(getattr(x, param) for param in sort_by))
                total = len(prod_list)
                products = prod_list[(page - 1) * per_page: page * per_page]
                pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
                return render_template('query_result.html', prod_list=products, pagination=pagination)
            else:
                flash('No products available')
                return redirect(url_for('product.product_view'))

    # Handle GET request
    products_query = Product.query.all()
    total = len(products_query)
    products = products_query[(page - 1) * per_page: page * per_page]
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
    return render_template('view_products.html', products=products, pagination=pagination)
