from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import inspect, text

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from app import routes, auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(routes.bp)
    
    with app.app_context():
        db.create_all()
        try:
            insp = inspect(db.engine)
            if 'sales' in insp.get_table_names():
                columns = [col['name'] for col in insp.get_columns('sales')]
                if 'vat_amount' not in columns:
                    db.session.execute(text('ALTER TABLE sales ADD COLUMN vat_amount FLOAT DEFAULT 0.0'))
                if 'staff_note' not in columns:
                    db.session.execute(text('ALTER TABLE sales ADD COLUMN staff_note TEXT'))
                db.session.commit()
        except Exception:
            db.session.rollback()
    
    return app
