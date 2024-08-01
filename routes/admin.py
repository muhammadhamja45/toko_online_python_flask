# routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, login_required
from app import db, bcrypt
from models import User, Product
from forms import AdminLoginForm
import os
from werkzeug.utils import secure_filename

bp = Blueprint('admin', __name__)

@bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.admin_dashboard'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.is_admin:
                login_user(user, remember=form.remember.data)
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('You do not have admin access.', 'danger')
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('admin_login.html', title='Admin Login', form=form)

@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.files['image']
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))
        else:
            image_filename = 'default.jpg'

        product = Product(name=name, price=price, image_file=image_filename)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    products = Product.query.all()
    return render_template('admin.html', products=products)

@bp.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if not current_user.is_admin:
        flash('You do not have access to perform this action.', 'danger')
        return redirect(url_for('shop.home'))

    db.session.delete(product)
    db.session.commit()
    flash('Product has been deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))
