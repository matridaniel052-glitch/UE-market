from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from functools import wraps
from .. import db
from ..models import Product
import os
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('⛔ Access denied! Admins only.')
            return redirect(url_for('shop.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/admin')
@login_required
@admin_required
def dashboard():
    products = Product.query.all()
    return render_template('admin.html', products=products)


@admin.route('/admin/add-product', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        description = request.form.get('description')
        stock = int(request.form.get('stock'))
        market = request.form.get('market')

        image_filename = 'default.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                image_filename = filename

        new_product = Product(
            name=name, price=price,
            category=category, description=description,
            stock=stock, image=image_filename, market=market
        )
        db.session.add(new_product)
        db.session.commit()
        flash('✅ Product added successfully!')
        return redirect(url_for('admin.dashboard'))

    return render_template('add_product.html')


@admin.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = float(request.form.get('price'))
        product.category = request.form.get('category')
        product.description = request.form.get('description')
        product.stock = int(request.form.get('stock'))
        product.market = request.form.get('market')

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                product.image = filename

        db.session.commit()
        flash('✅ Product updated successfully!')
        return redirect(url_for('admin.dashboard'))

    return render_template('edit_product.html', product=product)


@admin.route('/admin/delete/<int:id>')
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('🗑️ Product deleted!')
    return redirect(url_for('admin.dashboard'))