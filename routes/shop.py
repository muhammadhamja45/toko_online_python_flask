from flask import Blueprint, render_template, request
from models import Product



bp = Blueprint('shop', __name__)

@bp.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)
