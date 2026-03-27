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

# Prefer production automatically on Render when DJANGO_ENV is unset.
def get_runtime_environment() -> str:
    return os.getenv("DJANGO_ENV") or (
        "production" if os.getenv("RENDER", "").lower() == "true" else "development"
    )


env = get_runtime_environment()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"fishdex.settings.{env}")

application = get_asgi_application()
