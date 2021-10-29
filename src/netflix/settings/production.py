# Imports
try:
    from .base import *
    import os

except Exception as e:
    print(e)

# Set Debug to "False" in .env
DEBUG = os.environ['DEBUG']

# Allowed hosts in Cloud Services
ALLOWED_HOSTS = ['ip-address', 'https://Appurl.com/']           # NOTE:replace with actual address

# Database(Ignore for Cloud SQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.psycopg2',
        'NAME': 'netflix',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': ''
    }
}

# Production Server


# Django Inbuilt Security Vars

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
