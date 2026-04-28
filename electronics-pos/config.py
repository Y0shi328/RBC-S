import os

class Config:
    SECRET_KEY = 'your-secret-key-change-this'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pos_system.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
