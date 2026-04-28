#!/usr/bin/env python
"""
Initialize the POS system database with sample data.
Run this script once to set up the database with default users and products.
"""

from app import create_app, db
from app.models import User, Product

def init_database():
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional)
        # db.drop_all()
        
        # Create tables
        db.create_all()
        
        # Check if users already exist
        if User.query.filter_by(username='admin').first():
            print("Database already initialized with sample data!")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@electronicshop.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create employee user
        employee = User(
            username='employee',
            email='employee@electronicshop.com',
            role='employee'
        )
        employee.set_password('emp123')
        db.session.add(employee)
        
        # Sample products
        sample_products = [
            Product(name='iPhone 14 Case', category='phone-case', sku='PC-IP14-001', price=15.99, quantity_in_stock=50),
            Product(name='Samsung Galaxy Case', category='phone-case', sku='PC-SG-001', price=12.99, quantity_in_stock=45),
            Product(name='USB-C Fast Charger', category='charger', sku='CH-USBC-001', price=24.99, quantity_in_stock=30),
            Product(name='Wireless Charger', category='charger', sku='CH-WL-001', price=19.99, quantity_in_stock=25),
            Product(name='Lightning Cable', category='cable', sku='CB-LT-001', price=9.99, quantity_in_stock=100),
            Product(name='USB-C Cable', category='cable', sku='CB-USBC-001', price=8.99, quantity_in_stock=90),
            Product(name='Tempered Glass Screen Protector', category='screen-protector', sku='SP-TG-001', price=7.99, quantity_in_stock=60),
            Product(name='Privacy Screen Protector', category='screen-protector', sku='SP-PR-001', price=9.99, quantity_in_stock=40),
            Product(name='10000mAh Power Bank', category='power-bank', sku='PB-10K-001', price=29.99, quantity_in_stock=20),
            Product(name='20000mAh Power Bank', category='power-bank', sku='PB-20K-001', price=39.99, quantity_in_stock=15),
            Product(name='Bluetooth Speaker', category='other', sku='SP-BT-001', price=34.99, quantity_in_stock=18),
            Product(name='Phone Stand', category='other', sku='ST-PH-001', price=11.99, quantity_in_stock=35),
            Product(name='Screen Cleaning Kit', category='other', sku='CL-KIT-001', price=5.99, quantity_in_stock=50),
            Product(name='HDMI Cable', category='cable', sku='CB-HDMI-001', price=12.99, quantity_in_stock=25),
            Product(name='Car Phone Mount', category='other', sku='MN-CAR-001', price=14.99, quantity_in_stock=30),
        ]
        
        for product in sample_products:
            db.session.add(product)
        
        # Commit all changes
        db.session.commit()
        
        print("✅ Database initialized successfully!")
        print("\nDefault Credentials:")
        print("─" * 50)
        print("Admin User:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nEmployee User:")
        print("  Username: employee")
        print("  Password: emp123")
        print("─" * 50)
        print(f"\n✅ Added {len(sample_products)} sample products")
        print("\nYou can now run: python run.py")

if __name__ == '__main__':
    init_database()
