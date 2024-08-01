# seed_admin.py
from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()  # Membuat tabel jika belum ada
    
    # Mengecek apakah admin sudah ada
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        hashed_password = generate_password_hash('test', method='pbkdf2:sha256')
        admin = User(username='admin', password=hashed_password, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print(f"Admin user already exists. Username: {admin.username}, is_admin: {admin.is_admin}")
