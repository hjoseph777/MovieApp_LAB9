#!/bin/bash

# Build script for Render deployment
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running database migrations..."
python manage.py migrate

echo "Creating superuser if it doesn't exist..."
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

echo "Populating sample data..."
python manage.py populate_movies

echo "Running tests to verify build integrity..."
python manage.py test movie.tests --verbosity=1

echo "Build completed successfully!"