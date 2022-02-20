"""
WSGI config for netflix project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Load environment variables 
load_dotenv()

import os

from django.core.wsgi import get_wsgi_application

ServiceModule = os.getenv('SERVICE_MODULE')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", ServiceModule)

application = get_wsgi_application()
