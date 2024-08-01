import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Kunci rahasia untuk enkripsi data session
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    
    # URL database yang digunakan aplikasi
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    
    # Mematikan fitur track modifications untuk menghemat sumber daya
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Folder untuk upload file (gambar, dll)
    UPLOAD_FOLDER = 'static/images'
    
    # Konfigurasi untuk Google OAuth
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://127.0.0.1:5000/auth/callback')
