# production.py
"""
Production settings for Fishdex project.
"""

import os

import dj_database_url
from corsheaders.defaults import default_headers, default_methods

from . import base

# --- Copy all base uppercase settings into this module ---
for setting_name in dir(base):
    if setting_name.isupper():
        globals()[setting_name] = getattr(base, setting_name)

# --- Environment-specific overrides ---
DEBUG = False
os.environ["DJANGO_DEBUG"] = "False"

render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
configured_hosts = base.read_env_list("ALLOWED_HOSTS")
if render_hostname and render_hostname not in configured_hosts:
    configured_hosts.append(render_hostname)
ALLOWED_HOSTS = configured_hosts or ([render_hostname] if render_hostname else [])

CORS_ALLOWED_ORIGINS = base.read_env_list("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = base.read_env_list("CSRF_TRUSTED_ORIGINS")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ["content-type", "authorization"]
CORS_ALLOW_METHODS = list(default_methods) + ["OPTIONS"]

database_url = os.getenv("DATABASE_URL", "").strip()
if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            ssl_require=os.getenv("DATABASE_SSL_REQUIRE", "true").lower()
            not in {"0", "false", "no"},
        )
    }
else:
    database_host = os.getenv("DATABASE_HOST") or base.read_secret("pg_host")
    database_name = os.getenv("DATABASE_NAME") or base.read_secret("pg_db")
    database_user = os.getenv("DATABASE_USER") or base.read_secret("pg_user")
    database_password = os.getenv("DATABASE_PASSWORD") or base.read_secret(
        "pg_password"
    )
    database_port = os.getenv("DATABASE_PORT", "5432")

    if not all([database_host, database_name, database_user, database_password]):
        raise base.ImproperlyConfigured(
            "DATABASE_URL or DATABASE_HOST/DATABASE_NAME/DATABASE_USER/"
            "DATABASE_PASSWORD must be configured in production."
        )

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": database_name,
            "USER": database_user,
            "PASSWORD": database_password,
            "HOST": database_host,
            "PORT": database_port,
            "CONN_MAX_AGE": 600,
            "OPTIONS": {"sslmode": "require"},
        }
    }

base.LOGGING["handlers"]["console"]["formatter"] = "json"
base.LOGGING["root"]["handlers"] = ["console"]
base.LOGGING["root"]["level"] = "INFO"
base.LOGGING["loggers"]["django"]["level"] = "WARNING"

SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "true").lower() not in {
    "0",
    "false",
    "no",
}
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
