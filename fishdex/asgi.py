"""
ASGI config for frontend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

# import sys
# import logging

from django.core.asgi import get_asgi_application

# Parche seguro y temporal para entornos Docker/dev:
# Asegura un handler conectado a stdout muy temprano.
# En producción puedes eliminar o ajustar esto (usaremos dictConfig desde settings).
# logging.basicConfig(
#    level=logging.DEBUG,
#    stream=sys.stdout,
#    format="[%(levelname)s] %(asctime)s - %(name)s.%(funcName)s:%(lineno)d - %(message)s",
# )

env = os.getenv("DJANGO_ENV", "development")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"fishdex.settings.{env}")

application = get_asgi_application()
