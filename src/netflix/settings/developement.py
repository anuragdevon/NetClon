# Imports
from .base import *
import os

# DEBUG MODE (set it to "True" in dev mode)
DEBUG = os.environ['DEBUG']

# Allowed all local ports
ALLOWED_HOSTS = ['127.0.0.1']

# Local SQL Databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Developement server 
WSGI_APPLICATION = "netflix.wsgi.application"
