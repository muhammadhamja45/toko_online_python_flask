# routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user
from app import db, bcrypt, oauth
from models import User
from forms import RegistrationForm, LoginForm

bp = Blueprint('auth', __name__)

def register_google_oauth(app):
    google = oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        access_token_url='https://oauth2.googleapis.com/token',
        authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
        redirect_uri=app.config['GOOGLE_REDIRECT_URI'],
        client_kwargs={'scope': 'openid email profile'},
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
    )
    return google

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('shop.home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route('/google_login')
def google_login():
    google = register_google_oauth(current_app)
    redirect_uri = url_for('auth.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@bp.route('/auth/callback')
def google_callback():
    google = register_google_oauth(current_app)
    token = google.authorize_access_token()
    resp = google.get('https://www.googleapis.com/oauth2/v1/userinfo')  # URL lengkap untuk mendapatkan informasi pengguna
    user_info = resp.json()
    # Pastikan email dan username valid
    email = user_info['email']
    username = email.split('@')[0]  # Menggunakan nama sebelum '@' sebagai username
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash('default_password').decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash('Login successful!', 'success')
    return redirect(url_for('shop.home'))



@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('shop.home'))
