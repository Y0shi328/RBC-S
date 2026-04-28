# Electronics POS System

A web-based Point of Sale (POS) system for electronics shops with admin and employee account management.

## Features

✅ **Dual Account System**
- Admin account for managing products and viewing reports
- Employee account for processing sales

✅ **Core POS Features**
- Add/remove items from shopping cart
- Real-time stock management
- Quick checkout with automatic inventory updates
- Search products by name or category

✅ **Admin Features**
- Product management (create, update, delete)
- Inventory tracking
- Sales dashboard with key metrics
- Best-selling items report
- Daily and monthly sales trends

✅ **Employee Features**
- Simple and intuitive POS interface
- Quick product search
- Easy checkout process

✅ **Supported Products**
- Phone Cases
- Chargers & Cables
- Screen Protectors
- Power Banks
- Other Electronics

## Project Structure

```
electronics-pos/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── models.py              # Database models (User, Product, Sale, SaleItem)
│   ├── auth.py                # Authentication routes (login, register, logout)
│   ├── routes.py              # Main application routes and API endpoints
│   ├── templates/             # HTML templates
│   │   ├── login.html         # Login page
│   │   ├── register.html      # Registration page
│   │   ├── admin_dashboard.html
│   │   ├── employee_dashboard.html
│   │   ├── pos.html           # POS interface
│   │   ├── products.html      # Product management
│   │   └── reports.html       # Sales reports
│   └── static/
│       ├── css/
│       │   └── style.css      # Main stylesheet
│       └── js/
│           └── pos.js         # POS functionality (cart, checkout)
├── config.py                  # Flask configuration
├── run.py                      # Application entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file

```

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Navigate to the project directory:**
```bash
cd electronics-pos
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
```

3. **Activate the virtual environment:**

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (CMD):**
```cmd
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Run the application:**
```bash
python run.py
```

6. **Open your browser and go to:**
```
http://localhost:5000
```

## Default Credentials

### Admin Account (for testing)
- Username: `admin`
- Password: `admin123`
- Role: `admin`

### Employee Account (for testing)
- Username: `employee`
- Password: `emp123`
- Role: `employee`

**Note:** You can create new accounts using the registration page.

## Usage Guide

### For Admin Users

1. **Login** with admin credentials
2. **Manage Products:** 
   - Add new products with name, category, SKU, price, and stock quantity
   - Update existing products
   - Delete products
3. **View Dashboard:**
   - See total sales and transactions
   - View top-selling items
4. **Generate Reports:**
   - View best-selling products
   - Check daily and monthly sales trends

### For Employee Users

1. **Login** with employee credentials
2. **Process Sales:**
   - Search for products by name or category
   - Click "Add" to add items to cart
   - Use +/- buttons to adjust quantities
   - Click "Checkout" to complete the sale
3. **Cart Management:**
   - View cart with prices and quantities
   - Remove items if needed
   - Clear entire cart

## Database

- **Database Type:** SQLite (automatically created)
- **Database File:** `pos_system.db` (created in the project root)
- **Tables:**
  - `users` - User accounts and roles
  - `products` - Product inventory
  - `sales` - Sales transactions
  - `sale_items` - Individual items in each sale

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /logout` - Logout
- `GET /register` - Registration page
- `POST /register` - Create new account

### Dashboard
- `GET /` - Main dashboard (role-based)

### POS
- `GET /pos` - POS interface
- `POST /api/checkout` - Process checkout

### Products (Admin only)
- `GET /products` - Product management page
- `GET /api/products` - Get all products (JSON)
- `POST /api/products` - Create new product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Reports (Admin only)
- `GET /reports` - Sales reports and analytics

## Features in Detail

### Shopping Cart
- Add items with a single click
- Adjust quantities with +/- buttons
- Real-time price calculation
- Remove individual items
- Clear entire cart

### Inventory Management
- Stock automatically decreases after each sale
- "Out of Stock" button for unavailable items
- Stock levels visible in product list

### Sales Tracking
- Each sale recorded with:
  - Employee who made the sale
  - Items sold
  - Total amount
  - Timestamp

### Reports
- Best-selling products by quantity
- Revenue by product
- Daily sales summary
- Monthly sales trends
- Category-wise analysis

## Customization

### Adding New Product Categories
Edit `app/templates/products.html` in the product form:
```html
<select id="productCategory" required>
    <option value="your-category">Your Category</option>
    <!-- Add more categories here -->
</select>
```

### Changing Colors
Edit `app/static/css/style.css`:
- Primary color: `#667eea`
- Secondary color: `#2c3e50`
- Success color: `#27ae60`
- Error color: `#e74c3c`

### Adding Discounts
Modify the checkout logic in `app/routes.py` `checkout()` function to add discount calculations.

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to different port
```

### Database Issues
To reset the database, delete `pos_system.db` and restart the app.

### Import Errors
Make sure all packages are installed:
```bash
pip install -r requirements.txt
```

## Future Enhancements

- [ ] Receipt printing
- [ ] Discount codes
- [ ] Return/refund management
- [ ] Employee performance reports
- [ ] Multi-location support
- [ ] Mobile app
- [ ] Payment gateway integration
- [ ] Barcode scanning
- [ ] Email notifications

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, check the documentation above or contact the development team.

---

**Happy Selling! 🛒📱**
