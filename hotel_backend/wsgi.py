# hotel_backend/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_backend.settings')

# This variable MUST be named 'app' for Vercel to find it.
app = get_wsgi_application()