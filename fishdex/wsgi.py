"""
WSGI config for frontend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import logging
import sys


from django.core.wsgi import get_wsgi_application

# Configuración básica temprana para asegurar que stdout/stderr estén activos
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="[%(levelname)s] %(asctime)s - %(name)s.%(funcName)s:%(lineno)d - %(message)s",
)

env = os.getenv("DJANGO_ENV", "development")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"fishdex.settings.{env}")


application = get_wsgi_application()
