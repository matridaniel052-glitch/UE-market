from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..models import Product

shop = Blueprint('shop', __name__)

@shop.route('/')
def index():
    search = request.args.get('search', '')
    category = request.args.get('cat', '')
    market = request.args.get('market', '')

    query = Product.query

    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)
    if market:
        query = query.filter_by(market=market)

    products = query.all()
    return render_template('index.html', products=products,
                           search=search, category=category, market=market)

@shop.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    related = Product.query.filter_by(category=product.category).limit(4).all()
    return render_template('product.html', product=product, related=related)

@shop.route('/add-to-cart/<int:id>')
def add_to_cart(id):
    cart = session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    session['cart'] = cart
    session.modified = True
    flash('✅ Item added to cart!')
    return redirect(url_for('shop.product_detail', id=id))

@shop.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            subtotal = product.price * qty
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
            total += subtotal
    return render_template('cart.html', items=items, total=total)

@shop.route('/remove-from-cart/<int:id>')
def remove_from_cart(id):
    cart = session.get('cart', {})
    cart.pop(str(id), None)
    session['cart'] = cart
    flash('Item removed.')
    return redirect(url_for('shop.cart'))

@shop.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            subtotal = product.price * qty
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
            total += subtotal
    return render_template('checkout.html', items=items, total=total)

@shop.route('/place-order', methods=['POST'])
def place_order():
    session.pop('cart', None)
    flash('🎉 Order placed! We will contact you soon.')
    return redirect(url_for('shop.index'))