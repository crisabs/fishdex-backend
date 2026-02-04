# development.py
"""
Development settings for Fishdex project.
"""

import os
from . import base

# --- Copy all base uppercase settings into this module ---
for setting_name in dir(base):
    if setting_name.isupper():
        globals()[setting_name] = getattr(base, setting_name)

# --- Environment-specific overrides ---

DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in cors_origins.split(",") if origin.strip()
]
CORS_ALLOW_CREDENTIALS = True

ALLOWED_HOSTS = ["*"]

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

base.LOGGING["root"]["level"] = "DEBUG"
base.LOGGING["loggers"]["django"]["level"] = "DEBUG"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
