from flask import Blueprint, render_template, redirect,flash, send_from_directory
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename
from ecommweb.auth import login
from ecommweb.forms import ShopItemsForm, UpdateForm
from .models import Product, Order, Customer
from . import db

admin=Blueprint('admin',__name__)

@admin.route('/add-shop-items', methods=['GET','POST'])
@login_required
def add_shop_items():               
    if current_user.id==1:
        form=ShopItemsForm()
        if form.validate_on_submit():
            product_name=form.product_name.data
            current_price=form.current_price.data
            prev_price=form.prev_price.data
            in_stock=form.in_stock.data
            flash_sale=form.flash_sale.data
            
            file=form.product_picture.data

            file_name= secure_filename(file.filename)

            file_path=f'./media/{file_name}'

            file.save(file_path)

            new_shop_item=Product()  
            new_shop_item.product_name=product_name
            new_shop_item.current_price=float(current_price)  # Convert to float
            new_shop_item.previous_price=prev_price  # Changed from prev_price to previous_price
            new_shop_item.in_stock=in_stock
            new_shop_item.flash_sale=flash_sale
            new_shop_item.product_picture=file_path

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added successfully')
                print('Product Added')
                return redirect('/add-shop-items')  # Redirect after successful POST
            except Exception as e:
                print('Error:', str(e))  # Print the actual error
                flash('Product Not Added! Try Again')
                return redirect('/add-shop-items')
        return render_template('./add-shop-items.html', form=form)    
    return render_template('404.html')

@admin.route('/shop-items', methods=['GET','POST'])
@login_required
def shop_items():
    if current_user.id==1:
        items=Product.query.order_by(Product.date_added).all()
        return render_template('./shop-items.html', items=items)
    return render_template('404.html')

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)

@admin.route('/update-item/<int:item_id>', methods=['GET','POST'])
@login_required
def update_item(item_id):
    if current_user.id==1:
        form=ShopItemsForm()

        item_to_update= Product.query.get(item_id)

        form.product_name.render_kw = { 'placeholder': item_to_update.product_name}   
        form.prev_price.render_kw = { 'placeholder': item_to_update.previous_price}   
        form.current_price.render_kw = { 'placeholder': item_to_update.current_price}   
        form.in_stock.render_kw = { 'placeholder': item_to_update.in_stock}   
        form.flash_sale.render_kw = { 'placeholder': item_to_update.flash_sale}

        if form.validate_on_submit():
            product_name=form.product_name.data
            current_price=form.current_price.data
            previous_price=form.prev_price.data
            in_stock=form.in_stock.data
            flash_sale=form.flash_sale.data

            file=form.product_picture.data

            file_name=secure_filename(file.filename)
            file_path=f"./media/{file_name}"

            file.save(file_path)

            try:
                Product.query.filter_by(id=item_id).update(dict(product_name=product_name,
                current_price=current_price,
                previous_price=previous_price,
                in_stock=in_stock,
                flash_sale=flash_sale,
                product_picture=file_path))
                db.session.commit()
                flash(f'{product_name} updated succesfully')
                print('Product Updated')
                return redirect('/shop-items')
            except  Exception as e:
                print("Product Not Updated", e)
                flash('Product Not Updated! Try again')
        return render_template('update-item.html',form=form)
    return render_template('404.html')

@admin.route('/delete-item/<int:item_id>',methods=['GET','POST'])
@login_required
def delete_item(item_id):
    if current_user.id==1:
        try:
            if current_user.id == 1:
                item_to_delete=Product.query.get(item_id)
                db.session.delete(item_to_delete)
                db.session.commit()
                flash('Item Deleted Successfully')
                return redirect('/shop-items')
        except Exception as e:
            print("Item Not Deleted",e)
            flash('Item Not Deleted! Try Again')
        return redirect('/shop-items')
    return render_template('404.html')

@admin.route('/view-orders')
@login_required
def view_orders():
    if current_user.id==1:
        orders=Order.query.all()    
        return render_template('view-orders.html',orders=orders)
    return render_template('404.html')

@admin.route('/update-order/<int:order_id>', methods=['GET','POST'])
@login_required
def update_order(order_id):
    if current_user.id==1:
        form=UpdateForm()
        order=Order.query.get(order_id)

        if form.validate_on_submit():
            status=form.order_status.data
            order.status = status

            try:
                db.session.commit()
                flash('Order status updated successfully')
                return redirect('/view-orders')
            except Exception as e:
                flash(f'Order {order.id} not updated, Try Again')
                return redirect('/view-orders')


        return render_template('order-update.html',form=form)
    return render_template('404.html')

@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id==1:
        customers = Customer.query.all()
        return render_template('customer.html', customers=customers)

@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 1:
        return render_template('admin.html')
    return render_template('404.html')


