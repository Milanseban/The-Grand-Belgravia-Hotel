#!/bin/bash

# Exit on error
set -e

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy the local database to the writable /tmp directory
# This ensures our initial data (rooms, admin user) is available on Vercel
cp db.sqlite3 /tmp/db.sqlite3

# Run Django management commands
python manage.py collectstatic --no-input
python manage.py migrate