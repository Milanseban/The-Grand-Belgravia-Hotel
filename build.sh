#!/bin/bash

# Exit on any error
set -e

# Install dependencies
pip install -r requirements.txt

# Copy the database to the writable /tmp directory for the live server
cp db.sqlite3 /tmp/db.sqlite3

# Run Django management commands
python manage.py collectstatic --no-input
python manage.py migrate