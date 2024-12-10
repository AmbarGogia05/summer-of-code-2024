from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from app.models import db
from app.models.product import Product

product_blueprint = Blueprint('product', __name__)

@product_blueprint.route('/create/', methods=['GET','POST'])   
def create_product(): #to create a new product
    if request.method=='POST':
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
        except ValueError:
            flash('Invalid price or quantity!', 'error')
            return redirect(url_for('product.create_product'))

        new_prod = Product(Item_Name= name, Item_Description=desc, Item_Price=price, Item_Qty=qty)
        session['new_prod_id'] = new_prod.Item_SKU
        db.session.add(new_prod)
        db.session.commit()
        flash('Product added successfully')
        return redirect(url_for('product.create_product'))
    
    elif request.method=='GET':
        product = None
        if 'new_prod_id' in session:
            prod_id = session.pop('new_prod_id')
            product = Product.query.get(prod_id)
        return render_template('create_product.html', product=product)
    
@product_blueprint.route('/delete/', methods=['GET','POST'])
def delete_product():
    if request.method=='POST':
        sku = request.form['sku']

        prod = Product.query.get(sku)

        if prod:
            db.session.delete(prod)
            db.session.commit()
            flash('Product deleted successfully')
        else:
            flash('No such item')

        return redirect(url_for('product.delete_product'))

    elif request.method=='GET':
        return render_template('delete_product.html')
    
@product_blueprint.route('/update/', methods=['GET', 'POST'])
def update_product():
    if request.method=='POST':
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
            if price:
                prod.Item_Price = price
            if qty:
                prod.Item_Qty = qty
            session['prod_id'] = sku
            db.session.commit()
            flash('Update successful')
            return redirect(url_for('product.update_product'))
        else:
            flash('No such product')
            return redirect(url_for('product.update_product'))
        
    if request.method=='GET':
        prod = None
        if 'prod_id' in session:
            id = session.pop('prod_id')
            prod = Product.query.get(id)
        return render_template('update_product.html', product=prod)
    
@product_blueprint.route('/view/', methods=['GET', 'POST'])
def product_view():
    if request.method=='POST':
        sku = request.form['sku']
        name = request.form['name']
        if sku and not name:
            prod = Product.query.get(sku)
            if prod:
                prod_list=[prod]
                return render_template('query_result.html', prod_list = prod_list)
            else:
                flash('No such product')
                return redirect(url_for('product.product_view'))
        elif name and not sku:
            prod_list = Product.query.filter_by(Item_Name=name).all()
            if prod_list:
                return render_template('query_result.html', prod_list = prod_list)
            else:
                flash('No such product')
                return redirect(url_for('product.product_view'))
        elif name and sku:
            prod_list = Product.query.filter_by(Item_SKU=sku, Item_Name=name).all()
            if prod_list:
                return render_template('query_result.html', prod_list = prod_list)
            else:
                flash('No such product')
                return redirect(url_for('product.product_view'))
    if request.method=='GET':
        products = Product.query.all()
        return render_template('view_products.html', products=products)
    