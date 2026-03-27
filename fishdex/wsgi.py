"""
WSGI config for Fishdex project.

Exposes the WSGI callable as a module-level variable named `application`.

For more information, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
import logging

from django.core.wsgi import get_wsgi_application

# Early logging setup to ensure stdout/stderr capture
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="[%(levelname)s] %(asctime)s - %(name)s.%(funcName)s:%(lineno)d - %(message)s",
)

# Prefer production automatically on Render when DJANGO_ENV is unset.
def get_runtime_environment() -> str:
    return os.getenv("DJANGO_ENV") or (
        "production" if os.getenv("RENDER", "").lower() == "true" else "development"
    )


# Determine environment
env = get_runtime_environment()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"fishdex.settings.{env}")

application = get_wsgi_application()
