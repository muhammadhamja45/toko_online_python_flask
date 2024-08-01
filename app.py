from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)  # Inisialisasi OAuth dengan aplikasi Flask

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from models import User, Product, Order
        db.create_all()

    from routes.admin import bp as admin_bp
    from routes.shop import bp as shop_bp
    from routes.auth import bp as auth_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(auth_bp)

    return app
