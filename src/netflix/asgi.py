"""
ASGI config for netflix project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

"""Run ASGI Server Module"""
ServiceModule = os.getenv('SERVICE_MODULE')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", ServiceModule)
application = get_asgi_application()
