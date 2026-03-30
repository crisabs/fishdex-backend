#!/bin/sh
set -e

if [ -z "$DJANGO_ENV" ] && [ "${RENDER:-}" = "true" ]; then
    export DJANGO_ENV="production"
fi

echo "=============================="
echo "Iniciando FishDex ($DJANGO_ENV mode)"
echo "=============================="

APP_PORT="${PORT:-8000}"

# 1️⃣ Migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput
python manage.py create_superuser_if_not_exists


# 2️⃣ Collect static files en producción
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Recolectando archivos estáticos para producción..."
    python manage.py collectstatic --noinput
fi

# 3️⃣ Arrancar servidor
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Arrancando Gunicorn (producción)..."
    exec gunicorn fishdex.wsgi:application -c gunicorn_config.py --bind 0.0.0.0:${APP_PORT} --log-level info
else
    echo "Arrancando Django runserver (desarrollo)..."
    exec python manage.py runserver 0.0.0.0:${APP_PORT}
fi
