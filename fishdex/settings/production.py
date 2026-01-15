"""
Configuración específica para producción.
Usada cuando DJANGO_ENV=production.
"""

from .base import *  # noqa: F403, F401
from .base import read_secret, LOGGING
import os

# --- Desactivar DEBUG ---
DEBUG = False
os.environ["DJANGO_DEBUG"] = "False"
# --- Seguridad ---
# ⚠️ En producción, usa dominios específicos
ALLOWED_HOSTS = ["yourdomain.com", "api.yourdomain.com"]

# --- Base de datos (idéntica por ahora) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": read_secret("pg_db"),
        "USER": read_secret("pg_user"),
        "PASSWORD": read_secret("pg_password"),
        "HOST": "fishdex-postgres-db",
        "PORT": "5432",
    }
}

# --- Configuración extra futura ---
# - Cache (Redis o Memcached)
# - Logging avanzado
# - Compresión y CDN para archivos estáticos
# - Configuración de seguridad (SECURE_HSTS, CSRF_COOKIE_SECURE, etc.)

# --- Logging específico para producción ---
# Sobrescribimos para usar rotación de logs (archivos)
LOGGING["handlers"]["console"]["formatter"] = "json"  # formato JSON para monitorización
LOGGING["loggers"]["pokemon"]["handlers"] = ["console", "rotating_file"]
LOGGING["loggers"]["pokemon"]["level"] = "INFO"
LOGGING["loggers"]["django"]["level"] = "WARNING"  # Django solo errores o avisos
LOGGING["root"]["handlers"] = ["console", "rotating_file"]
LOGGING["root"]["level"] = "INFO"
