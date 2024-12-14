from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from app.models import db
from app.models.customer import Customer
from app.models.product import Product
from app.models.staff import Staff
from app.models.transaction import Transaction, TransactionItem, TransactionHistory
from flask_login import login_required, current_user
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from sqlalchemy.exc import OperationalError

transaction_blueprint = Blueprint('transaction', __name__)

def process_transaction(item_list_sorted, c_ID, s_ID, t_ID=None):
    try:
        customer = Customer.query.filter_by(c_ID=c_ID).with_for_update().one_or_none()
        if customer is None:
            flash(f'Customer with ID {c_ID} not found!', 'error')
            return 'error'
        transaction_object = Transaction(c_id=c_ID, s_id=s_ID, total_amount=0)
        if t_ID:
            transaction_object.t_id = t_ID
        jsontype_list = []
        for (sku, quantity) in item_list_sorted:
            try:
                sku = int(sku)
                if sku <= 0:
                    raise ValueError
            except ValueError:
                flash('Please input a positive integer as SKU!', "error")
                db.session.rollback()
                return "error"

            try:
                quantity = int(quantity)
                product = Product.query.filter_by(Item_SKU=sku).with_for_update().one()
            except ValueError:
                flash('Please input a positive integer as quantity!', "error")
                db.session.rollback()
                return "error"
            except OperationalError as e:  # Handle deadlock or lock timeout
                db.session.rollback()
                return "retry"  # Signal to retry the transaction
            except Exception:
                db.session.rollback()
                flash(f'Product with SKU {sku} not found!', "error")
                return "error"
            
            if quantity > product.Item_Qty:
                flash(f'Max quantity available for product {sku} is {product.Item_Qty}!', "error")
                db.session.rollback()
                return "error"
            
            product.Item_Qty -= quantity
            item = TransactionItem(product_SKU=sku, quantity=quantity, amount=product.Item_Price * quantity)
            transaction_object.items.append(item)
            transaction_object.total_amount += item.amount
            jsontype_list.append([sku, quantity])

        db.session.add(transaction_object)
        transactionlog = TransactionHistory(t_id=transaction_object.t_id, c_id=transaction_object.c_id, s_id=transaction_object.s_id, date=transaction_object.date, time=transaction_object.time, total_amount=transaction_object.total_amount, items=jsontype_list)
        db.session.add(transactionlog)
        db.session.commit()
        return "success"

    except OperationalError as e:  # Handle deadlocks at the outer level
        db.session.rollback()
        return "retry"  # Signal the outer loop to retry

    except Exception as e:
        db.session.rollback()
        flash('An unexpected error occurred during the transaction!', "error")
        return "error"



@transaction_blueprint.route('/create/', methods=['GET', 'POST'])
@login_required #flask-login protects the route
def create_transaction():
    verify_jwt_in_request()
    jwt_identity = get_jwt_identity()

    if jwt_identity['role'] != 'staff':
        flash('Not authorized to create transactions!')
        return redirect(url_for('customer.login'))

    else:
        if request.method == 'POST':
            c_ID = request.form['c_ID']
            skus = request.form.getlist('sku[]')
            quantities = request.form.getlist('quantity[]')
            s_ID = jwt_identity['id']
            transaction_items = list(zip(skus, quantities))
            transaction_items.sort(key=lambda x: x[0])
            retry_count = 0
            while retry_count<5:
                response = process_transaction(transaction_items, c_ID, s_ID)
                if response == "success":
                    flash("Successfully created transaction!", "success")
                    session.pop('transaction_data', None)
                    return redirect(url_for('transaction.create_transaction'))
                elif response == "error" or retry_count==5:
                    if retry_count == 5:
                        flash("Transaction failed due to conflicting requests", "error")
                    else:
                        flash("Transaction failed!", "error")
                    session['transaction_data'] = {'c_ID': c_ID, 'skus': skus, 'quantities': quantities}
                    return redirect(url_for('transaction.create_transaction'))
                else:
                    retry_count += 1
                    continue

        if request.method == 'GET':
            transaction_data = session.get('transaction_data', {})
            session.pop('transaction_data', None)
            return render_template('create_transaction.html', transaction_data=transaction_data)
        
def transaction_remover(t_ID):
    transaction = Transaction.query.get(t_ID)
    if not transaction:
        return "transaction_not_found"
    try:
        transaction_items = TransactionItem.query.filter_by(transaction_id=t_ID).all()
        for item in transaction_items:
            product = Product.query.get(item.product_SKU)
            product.Item_Qty += item.quantity
            db.session.delete(item)
        db.session.delete(transaction)
        db.session.commit()
        return "success"
    except Exception as e:
        db.session.rollback()
        return "error"

@transaction_blueprint.route('/delete', methods=['GET','POST'])
@login_required
def delete_transaction():
    jwt_identity = get_jwt_identity()
    if jwt_identity['role'] != 'staff':
            flash("Unauthorized access", "error")
            return redirect(url_for('customer.home'))
    elif jwt_identity['isadmin']:
        if request.method == 'POST':
            t_ID = request.form.get('t_ID')
            
            counter = 1
            while counter <= 5:
                obj = transaction_remover(t_ID)
                if obj == "transaction_not_found":
                    flash('No transaction with given ID', 'error')
                    return redirect(url_for('transaction.delete_transaction'))
                elif obj == "error" and counter == 5:
                    flash("An error occured, please try again!", 'error')
                    return redirect(url_for('transaction.delete_transaction'))
                elif obj == "error":
                    counter += 1
                    continue
                else:
                    flash("Successfully deleted transaction", 'success')
                    return redirect(url_for('transaction.delete_transaction'))

        else:
            return render_template('delete_transaction.html')

@transaction_blueprint.route('/find/', methods=['GET', 'POST'])
@login_required
def find_transaction():
    verify_jwt_in_request()
    jwt_identity = get_jwt_identity()

    if jwt_identity['role'] != 'staff':
        flash('Not authorized to view and update transactions!')
        return redirect(url_for('customer.login'))
    if request.method == 'POST':
        t_ID = request.form['t_ID']
        try:
            t_ID=int(t_ID)
        except ValueError:
            flash('Please input a valid transaction ID!', 'error')
            return(redirect(url_for('transaction.find_transaction')))
        transaction = Transaction.query.get(t_ID)
        transaction_items = TransactionItem.query.filter_by(transaction_id = t_ID).all()
        if transaction:
            return render_template('view_and_update_transaction.html', transaction=transaction, transaction_items=transaction_items)
        else:
            flash('No such transaction', 'error')
            return redirect(url_for('transaction.find_transaction'))
    if request.method == 'GET':
        return render_template('find_transaction.html')

@transaction_blueprint.route('/update/', methods=['GET', 'POST'])
@login_required
def update_transaction():
    if request.method == 'GET':
        return redirect(url_for('transaction.find_transaction'))
    elif request.method == 'POST':
        verify_jwt_in_request()
        jwt_identity = get_jwt_identity()

        if jwt_identity['role'] != 'staff':
            flash('Not authorized to view and update transactions!')
            return redirect(url_for('customer.login'))
        
        t_id = request.form['t_ID']
        c_ID = request.form['c_ID']
        s_ID_new = jwt_identity['id']
        skus_new = request.form.getlist('sku[]')
        quantities_new = request.form.getlist('quantity[]')
        transaction_items_new = list(zip(skus_new, quantities_new))
        transaction_items_new.sort(key=lambda x: x[0])
        
        counter = 0
        while counter <= 5:
                obj = transaction_remover(t_id)
                if obj == "error" and counter == 5:
                    flash("An error occured, please try again!", 'error')
                    return redirect(url_for('transaction.update_transaction'))
                elif obj == "error":
                    counter += 1
                    continue
                else:
                    break
        
        retry_count = 0
        while retry_count<5:
            response = process_transaction(transaction_items_new, c_ID, s_ID_new, t_id)
            if response == "success":
                flash("Successfully updated transaction!", "success")
                return redirect(url_for('transaction.find_transaction'))
            elif response == "error" or retry_count==5:
                if retry_count == 5:
                    flash("Transaction update failed due to conflicting requests", "error")
                    return redirect(url_for('transaction.find_transaction'))
                else:
                    flash("Transaction update failed!", "error")
                    return redirect(url_for('transaction.find_transaction'))
            else:
                retry_count += 1
                continue
        