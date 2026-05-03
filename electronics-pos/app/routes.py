from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Product, Sale, SaleItem, User
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

bp = Blueprint('routes', __name__)

# Dashboard
@bp.route('/')
@login_required
def dashboard():
    if current_user.role == 'admin':
        total_sales = db.session.query(func.sum(Sale.total_amount)).scalar() or 0
        total_transactions = Sale.query.count()

        top_products = db.session.query(
            Product.name,
            func.sum(SaleItem.quantity).label('total_qty'),
            func.sum(SaleItem.subtotal).label('total_sales')
        ).join(SaleItem).group_by(Product.id).order_by(
            func.sum(SaleItem.quantity).desc()
        ).limit(5).all()

        # ✅ INVENTORY STATS (CLEAN VERSION USING YOUR MODEL METHOD)
        products = Product.query.all()

        in_stock = 0
        low_stock = 0
        critical_stock = 0
        out_of_stock = 0
        total_inventory = 0

        for p in products:
            total_inventory += p.quantity_in_stock

            status = p.get_stock_status()

            if status == 'out_of_stock':
                out_of_stock += 1
            elif status == 'critical_stock':
                critical_stock += 1
            elif status == 'low_stock':
                low_stock += 1
            else:
                in_stock += 1

        return render_template('admin_dashboard.html', 
            total_sales=total_sales,
            total_transactions=total_transactions,
            top_products=top_products,

            # inventory stats
            total_inventory=total_inventory,
            in_stock=in_stock,
            low_stock=low_stock,
            critical_stock=critical_stock,
            out_of_stock=out_of_stock
        )

    else:
        # Employee Dashboard
        today = datetime.now().date()

        today_sales = db.session.query(func.sum(Sale.total_amount)).filter(
            Sale.employee_id == current_user.id,
            func.date(Sale.created_at) == today
        ).scalar() or 0

        total_sales = db.session.query(func.sum(Sale.total_amount)).filter(
            Sale.employee_id == current_user.id
        ).scalar() or 0

        transaction_count = Sale.query.filter(
            Sale.employee_id == current_user.id
        ).count()

        items_sold = db.session.query(func.sum(SaleItem.quantity)).join(
            Sale, SaleItem.sale_id == Sale.id
        ).filter(
            Sale.employee_id == current_user.id
        ).scalar() or 0

        user_sales = Sale.query.filter(
            Sale.employee_id == current_user.id
        ).order_by(Sale.created_at.desc()).limit(5).all()

        return render_template('employee_dashboard.html',
            today_sales=today_sales,
            total_sales=total_sales,
            transaction_count=transaction_count,
            items_sold=items_sold,
            user_sales=user_sales
        )

# POS - Add to Cart
@bp.route('/pos')
@login_required
def pos():
    products = Product.query.all()
    return render_template('pos.html', products=products)

@bp.route('/api/checkout', methods=['POST'])
@login_required
def checkout():
    data = request.json
    items = data.get('items', [])
    
    if not items:
        return jsonify({'error': 'No items in cart'}), 400
    
    try:
        total_amount = 0
        total_items = 0
        sale = Sale(employee_id=current_user.id, items_count=0, total_amount=0)
        
        for item in items:
            product = Product.query.get(item['product_id'])
            if not product:
                return jsonify({'error': f'Product {item["product_id"]} not found'}), 400
            
            if product.quantity_in_stock < item['quantity']:
                return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
            
            subtotal = product.price * item['quantity']
            sale_item = SaleItem(
                product_id=product.id,
                quantity=item['quantity'],
                unit_price=product.price,
                subtotal=subtotal
            )
            
            product.quantity_in_stock -= item['quantity']
            total_amount += subtotal
            total_items += item['quantity']
            
            sale.items.append(sale_item)
        
        sale.total_amount = total_amount
        sale.items_count = total_items
        
        db.session.add(sale)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'sale_id': sale.id,
            'total_amount': total_amount,
            'items_count': total_items
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Products Management (Admin only)
@bp.route('/products')
@login_required
def products():
    if current_user.role != 'admin':
        flash('Only admins can manage products', 'error')
        return redirect(url_for('routes.dashboard'))
    
    products = Product.query.all()
    return render_template('products.html', products=products)

@bp.route('/api/products', methods=['POST'])
@login_required
def add_product():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    product = Product(
        name=data['name'],
        category=data['category'],
        sku=data['sku'],
        price=float(data['price']),
        quantity_in_stock=int(data['quantity'])
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'success': True, 'product_id': product.id})

@bp.route('/api/products/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.json
    product.name = data.get('name', product.name)
    product.category = data.get('category', product.category)
    product.price = float(data.get('price', product.price))
    product.quantity_in_stock = int(data.get('quantity', product.quantity_in_stock))
    
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/api/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({'success': True})

# Reports
@bp.route('/reports')
@login_required
def reports():
    if current_user.role == 'admin':
        # Admin sees all reports
        best_sellers = db.session.query(
            Product.name,
            Product.category,
            func.sum(SaleItem.quantity).label('total_qty'),
            func.sum(SaleItem.subtotal).label('total_sales')
        ).join(SaleItem).group_by(Product.id).order_by(func.sum(SaleItem.quantity).desc()).all()
        
        # Daily sales
        today = datetime.utcnow().date()
        daily_sales = Sale.query.filter(
            func.date(Sale.created_at) == today
        ).all()
        daily_total = sum(s.total_amount for s in daily_sales)
        
        # Monthly sales
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        monthly_sales = db.session.query(
            func.date(Sale.created_at).label('date'),
            func.sum(Sale.total_amount).label('total')
        ).filter(Sale.created_at >= thirty_days_ago).group_by(func.date(Sale.created_at)).all()
        #  INVENTORY STATS (FIXED LOCATION)
        products = Product.query.all()

        in_stock = 0
        low_stock = 0
        critical_stock = 0
        out_of_stock = 0

        for p in products:
            status = p.get_stock_status()

            if status == 'out_of_stock':
                out_of_stock += 1
            elif status == 'critical_stock':
                critical_stock += 1
            elif status == 'low_stock':
                low_stock += 1
            else:
                in_stock += 1
        
        return render_template('reports.html',
                             best_sellers=best_sellers,
                             daily_sales=daily_total,
                             monthly_sales=monthly_sales,
                             in_stock=in_stock,
                             low_stock=low_stock,
                             critical_stock=critical_stock,
                             out_of_stock=out_of_stock,
                             user_role='admin')
    else:
        # Employee sees their own reports
        best_sellers = db.session.query(
            Product.name,
            Product.category,
            func.sum(SaleItem.quantity).label('total_qty'),
            func.sum(SaleItem.subtotal).label('total_sales')
        ).join(SaleItem).join(Sale).filter(
            Sale.employee_id == current_user.id
        ).group_by(Product.id).order_by(func.sum(SaleItem.quantity).desc()).all()
        
        # Daily sales for employee
        today = datetime.utcnow().date()
        daily_sales = Sale.query.filter(
            Sale.employee_id == current_user.id,
            func.date(Sale.created_at) == today
        ).all()
        daily_total = sum(s.total_amount for s in daily_sales)
        
        # Monthly sales for employee
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        monthly_sales = db.session.query(
            func.date(Sale.created_at).label('date'),
            func.sum(Sale.total_amount).label('total')
        ).filter(
            Sale.employee_id == current_user.id,
            Sale.created_at >= thirty_days_ago
        ).group_by(func.date(Sale.created_at)).all()
        
        # INVENTORY STATS (SAME AS ADMIN)
        products = Product.query.all()
        
        in_stock = 0
        low_stock = 0
        critical_stock = 0
        out_of_stock = 0
        
        for p in products:
            status = p.get_stock_status()
            
            if status == 'out_of_stock':
                out_of_stock += 1
            elif status == 'critical_stock':
                critical_stock += 1
            elif status == 'low_stock':
                low_stock += 1
            else:
                in_stock += 1
        
        return render_template('reports.html',
                             best_sellers=best_sellers,
                             daily_sales=daily_total,
                             monthly_sales=monthly_sales,
                             in_stock=in_stock,
                             low_stock=low_stock,
                             critical_stock=critical_stock,
                             out_of_stock=out_of_stock,
                             user_role='employee')

# Get all products for API
@bp.route('/api/products')
@login_required
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'category': p.category,
        'price': p.price,
        'quantity': p.quantity_in_stock
    } for p in products])

# Profile Page
@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()

    if not username or not email:
        return jsonify({'error': 'Username and email are required.'}), 400

    current_user.username = username
    current_user.email = email

    try:
        db.session.commit()
        return jsonify({'success': True})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'That username or email is already in use.'}), 400

@bp.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('currentPassword', '')
    new_password = request.form.get('newPassword', '')
    confirm_password = request.form.get('confirmPassword', '')

    if not current_password or not new_password or not confirm_password:
        return jsonify({'error': 'Please fill in all password fields.'}), 400

    if new_password != confirm_password:
        return jsonify({'error': 'New password and confirmation do not match.'}), 400

    if not current_user.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect.'}), 400

    current_user.set_password(new_password)
    db.session.commit()
    return jsonify({'success': True})

# Users Page (Admin only)
@bp.route('/users')
@login_required
def users():
    if current_user.role != 'admin':
        flash('Only admins can view users', 'error')
        return redirect(url_for('routes.dashboard'))
    
    all_users = User.query.all()
    return render_template('users.html', users=all_users)
