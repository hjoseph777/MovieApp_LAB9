# CineVault - Setup & Deployment Guide

This document provides comprehensive instructions for setting up the Django Movie Collection application locally and deploying it to production.

## Local Development Setup

### Prerequisites

- Python 3.11+
- pip
- Git

### Step-by-Step Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd MovieApp_LAB9
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env file with your settings
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Create sample data:**
```bash
python manage.py populate_movies
```

7. **Create superuser (optional):**
```bash
python manage.py createsuperuser
```

8. **Run development server:**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the application.

## Production Deployment on Render

This application is configured for easy deployment on Render.com:

### Environment Variables Setup

Set these in your Render service dashboard:

**Required Variables:**
- `SECRET_KEY`: Your Django secret key (generate new for production)
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `your-app.onrender.com`

**Optional Variables (Render provides automatically):**
- `DATABASE_URL`: PostgreSQL database URL (auto-configured by Render)

### Render Service Configuration

**Build Settings:**
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn movieapp_lab9.wsgi:application`
- **Environment**: `Python`

### Automated Build Process

The build script (`build.sh`) automatically:
- Installs dependencies
- Collects static files
- Runs database migrations
- Creates admin user (username: admin, password: admin123)
- Populates sample movie data

### Post-Deployment Verification

1. Verify the application loads
2. Test navigation menu functionality
3. Test movie listing and search features
4. Access admin panel with admin/admin123
5. Update admin password for security

## Render Deployment Checklist

## ✅ Required Files for Render Deployment

### Core Application Files
- [x] `manage.py` - Django management script
- [x] `movieapp_lab9/` - Django project directory
  - [x] `settings.py` - Production-ready settings
  - [x] `urls.py` - URL configuration
  - [x] `wsgi.py` - WSGI application
- [x] `movie/` - Django app directory

### Deployment Configuration Files
- [x] `requirements.txt` - Python dependencies
- [x] `Procfile` - Process configuration for Render
- [x] `build.sh` - Build script (executable)
- [x] `runtime.txt` - Python version specification
- [x] `.gitignore` - Git ignore patterns
- [x] `.env.example` - Environment variables template
- [x] `README.md` - Project documentation

### Dependencies in requirements.txt
- [x] `Django==5.2.8` - Web framework
- [x] `gunicorn==21.2.0` - WSGI server
- [x] `psycopg2-binary==2.9.9` - PostgreSQL adapter
- [x] `whitenoise==6.6.0` - Static files serving
- [x] `python-decouple==3.8` - Environment variables
- [x] `dj-database-url==2.1.0` - Database URL parsing

## 📋 Environment Variables for Render

Set these in your Render service dashboard:

### Required
- `SECRET_KEY` - Django secret key (generate new for production)
- `DEBUG` - Set to `False`
- `ALLOWED_HOSTS` - Your Render app URL (e.g., `your-app.onrender.com`)

### Optional (Render provides DATABASE_URL automatically)
- `DATABASE_URL` - PostgreSQL database URL (auto-configured by Render)

## 🚀 Render Service Configuration

### Build Settings
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn movieapp_lab9.wsgi:application`
- **Environment**: `Python`

### What the build script does:
1. Installs Python dependencies
2. Collects static files
3. Runs database migrations
4. Creates admin superuser (admin/admin123)
5. Populates sample movie data

## 🔧 Features Verified
- [x] Responsive design with mobile support
- [x] Static files properly served with WhiteNoise
- [x] Database migrations configured
- [x] Admin interface accessible
- [x] Sample data populated automatically
- [x] Environment-based configuration (dev vs production)
- [x] HTTPS-ready (Render provides SSL)

## 📝 Post-Deployment Steps

1. Verify the application loads
2. Test navigation menu functionality
3. Test movie listing and search features
4. Access admin panel with admin/admin123
5. Update admin password for security

## 🛠️ Local Testing Before Deploy

```bash
# Test with production-like settings
export DEBUG=False
export ALLOWED_HOSTS=127.0.0.1,localhost
python manage.py collectstatic --noinput
python manage.py runserver
```

## 📱 Application URLs

- `/` - Homepage
- `/movies/` - All movies listing
- `/search/` - Search by genre
- `/movie/<id>/` - Individual movie details
- `/admin/` - Django admin interface

Everything is ready for GitHub push and Render deployment! 🚀