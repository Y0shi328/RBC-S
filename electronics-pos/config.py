import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    
    # Database configuration - supports both local SQLite and Render PostgreSQL
    if os.environ.get('DATABASE_URL'):
        # Render uses DATABASE_URL for PostgreSQL
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        # Local development uses SQLite
        SQLALCHEMY_DATABASE_URI = 'sqlite:///pos_system.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
