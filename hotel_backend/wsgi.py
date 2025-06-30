import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_backend.settings')

# The 'application' variable is what the server uses.
# We are wrapping the default Django application with WhiteNoise.
from whitenoise import WhiteNoise
application = get_wsgi_application()
application = WhiteNoise(application)