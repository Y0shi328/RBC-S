# Render Deployment Guide

## Prerequisites
- Render.com account
- Git repository with your code

## Steps to Deploy on Render

### 1. Create PostgreSQL Database on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Give it a name (e.g., `pos-system-db`)
4. Select region and plan
5. Click "Create Database"
6. Copy the "External Database URL" (looks like `postgresql://...`)

### 2. Create Web Service on Render
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: e.g., `pos-system`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:create_app()`
   - **Region**: Same as your database

### 3. Add Environment Variables
In the Render Web Service dashboard, go to **Environment** and add:

```
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

(Paste the PostgreSQL External URL from step 1)

### 4. Deploy the Database Schema
After deployment, run migrations by opening a shell on Render or using the Render CLI:

```bash
# If using Render Shell
python init_db.py
```

Or manually create the database by accessing your Flask app's shell context.

### 5. Important Files for Render
- `requirements.txt` - Updated with `psycopg2-binary` for PostgreSQL
- `config.py` - Now reads `DATABASE_URL` environment variable
- `Procfile` (optional) - For more control over startup

## Troubleshooting

### Database Connection Issues
- Make sure DATABASE_URL is set in Render environment variables
- Check the External Database URL format: `postgresql://user:password@host:port/dbname`
- Verify PostgreSQL credentials are correct

### Migrations/Schema Issues
- Use `init_db.py` to create tables on Render
- Or run migrations if using Flask-Migrate

## Local Development
For local development, the app automatically uses SQLite (`pos_system.db`). 
No DATABASE_URL needed - just run normally:

```bash
python run.py
```

## Production Checklist
- [ ] DATABASE_URL set in Render environment
- [ ] SECRET_KEY set to a strong random value
- [ ] Database tables initialized
- [ ] Test login/operations work
- [ ] Check Render logs for errors
