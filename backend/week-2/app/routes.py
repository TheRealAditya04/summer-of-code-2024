from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from .models import db, InventoryItem, Staff
from .forms import ProductForm
from flask_wtf.csrf import validate_csrf
from werkzeug.exceptions import BadRequest
from .decorators import login_required, admin_required

# Product Blueprint
product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['GET'])
@login_required
def list_products():
    products = InventoryItem.query.all()
    form = ProductForm()  # Create an instance of the form
    return render_template('products/list.html', products=products, form=form)


# Add a new product
@product_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = ProductForm()  # Ensure the form is instantiated here
    if form.validate_on_submit():
        new_product = InventoryItem(
            item_name=form.name.data,
            item_description=form.description.data,
            item_price=form.price.data,
            item_qty=form.quantity.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('product_bp.list_products'))
    return render_template('products/add.html', form=form)


# Edit a product
@product_bp.route('/products/edit/<string:item_sku>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(item_sku):
    product = InventoryItem.query.filter_by(item_sku=item_sku).first()
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('product_bp.list_products'))

    form = ProductForm(
        name=product.item_name,
        description=product.item_description,
        price=product.item_price,
        quantity=product.item_qty
    )
    if form.validate_on_submit():
        product.item_name = form.name.data
        product.item_description = form.description.data
        product.item_price = form.price.data
        product.item_qty = form.quantity.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product_bp.list_products'))

    return render_template('products/edit.html', form=form, product=product)


# Delete a product
@product_bp.route('/products/delete/<string:item_sku>', methods=['POST'])
@login_required
@admin_required
def delete_product(item_sku):
    try:
        validate_csrf(request.form.get('csrf_token'))
    except BadRequest:
        flash('CSRF token missing or invalid!', 'danger')
        return redirect(url_for('product_bp.list_products'))

    product = InventoryItem.query.filter_by(item_sku=item_sku).first()
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('product_bp.list_products'))

    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('product_bp.list_products'))


# Auth Blueprint

