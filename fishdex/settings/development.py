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

CORS_ALLOWED_ORIGINS = base.read_env_list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = True

ALLOWED_HOSTS = ["*"]

database_host = os.getenv("DATABASE_HOST", "fishdex-postgres-db")
database_name = os.getenv("DATABASE_NAME") or base.read_secret("pg_db")
database_user = os.getenv("DATABASE_USER") or base.read_secret("pg_user")
database_password = os.getenv("DATABASE_PASSWORD") or base.read_secret("pg_password")
database_port = os.getenv("DATABASE_PORT", "5432")

if all([database_name, database_user, database_password]):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": database_name,
            "USER": database_user,
            "PASSWORD": database_password,
            "HOST": database_host,
            "PORT": database_port,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": base.BASE_DIR / "db.sqlite3",
        }
    }

base.LOGGING["root"]["level"] = "DEBUG"
base.LOGGING["loggers"]["django"]["level"] = "DEBUG"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
