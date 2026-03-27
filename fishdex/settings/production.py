# production.py
"""
Production settings for Fishdex project.
"""

import os
from . import base


from corsheaders.defaults import default_headers, default_methods

CORS_ALLOW_HEADERS = list(default_headers) + [
    "content-type",
    "authorization",
]

CORS_ALLOW_METHODS = list(default_methods) + ["OPTIONS"]

# --- Copy all base uppercase settings into this module ---
for setting_name in dir(base):
    if setting_name.isupper():
        globals()[setting_name] = getattr(base, setting_name)

# --- Environment-specific overrides ---
DEBUG = False
os.environ["DJANGO_DEBUG"] = "False"

CORS_ALLOWED_ORIGINS = [
    "https://fishdex-frontend.onrender.com",
    "https://www.fishdex-frontend.onrender.com",
]

ALLOWED_HOSTS = [
    "fishdex-backend-pww8.onrender.com",
    "www.fishdex-backend-pww8.onrender.com",
]

CORS_ALLOW_CREDENTIALS = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": base.read_secret("pg_db"),
        "USER": base.read_secret("pg_user"),
        "PASSWORD": base.read_secret("pg_password"),
        "HOST": "fishdex-postgres-db",
        "PORT": "5432",
    }
}

base.LOGGING["handlers"]["console"]["formatter"] = "json"
base.LOGGING["root"]["handlers"] = ["console", "rotating_file"]
base.LOGGING["root"]["level"] = "INFO"
base.LOGGING["loggers"]["django"]["level"] = "WARNING"
