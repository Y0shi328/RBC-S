# Quick Start Guide - Electronics POS System

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python init_db.py
```

This will:
- Create the SQLite database
- Create 2 default accounts (admin & employee)
- Add 15 sample electronics products

### Step 3: Run the Application
```bash
python run.py
```

Then open your browser to: **http://localhost:5000**

---

## 🔐 Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Employee Account:**
- Username: `employee`
- Password: `emp123`

---

## 📋 Sample Products Included

The database comes pre-loaded with:
- ✅ Phone Cases (iPhone 14, Samsung Galaxy)
- ✅ Chargers (USB-C, Wireless)
- ✅ Cables (Lightning, USB-C, HDMI)
- ✅ Screen Protectors (Tempered Glass, Privacy)
- ✅ Power Banks (10000mAh, 20000mAh)
- ✅ Accessories (Speaker, Phone Stand, Car Mount)

---

## 🎯 What You Can Do

### As Admin:
1. ✅ Add/Edit/Delete products
2. ✅ View sales dashboard
3. ✅ See best-selling products
4. ✅ View daily/monthly reports

### As Employee:
1. ✅ Search products quickly
2. ✅ Add items to cart
3. ✅ Complete sales
4. ✅ Print receipts (future)

---

## 📁 Project Files

```
electronics-pos/
├── run.py                    ← Start here: python run.py
├── init_db.py               ← Initialize database: python init_db.py
├── config.py                ← Configuration settings
├── requirements.txt         ← Python packages needed
├── app/
│   ├── models.py            ← Database models
│   ├── auth.py              ← Login/Register
│   ├── routes.py            ← Main app logic
│   ├── templates/           ← HTML pages
│   └── static/              ← CSS & JavaScript
└── README.md                ← Full documentation
```

---

## 🐛 Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'flask'`
```bash
pip install -r requirements.txt
```

**Problem:** Port 5000 already in use
- Edit `run.py` and change port to 5001, 5002, etc.

**Problem:** Database issues
```bash
# Delete the database and reinitialize
rm pos_system.db
python init_db.py
python run.py
```

---

## 📚 Next Steps

1. Try logging in with both accounts
2. Add a few products as admin
3. Process a sale as employee
4. Check the reports dashboard
5. Customize colors in `app/static/css/style.css`

Enjoy! 🎉
