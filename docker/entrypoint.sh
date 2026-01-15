#!/bin/sh
set -e

echo "=============================="
echo "Iniciando FishDex ($DJANGO_ENV mode)"
echo "=============================="

# 1️⃣ Esperar a que PostgreSQL esté disponible
HOST="${DATABASE_HOST:-fishdex-postgres-db}"
PORT="${DATABASE_PORT:-5432}"

echo "Esperando a que Postgres esté disponible en ${HOST}:${PORT}..."
while ! python3 - <<PY
import socket, sys
try:
    s = socket.create_connection(("${HOST}", int("${PORT}")), timeout=1)
    s.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
do
  echo "Postgres no disponible todavía, reintentando en 2s..."
  sleep 2
done
echo "Base de datos disponible."

# 2️⃣ Migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput

# 3️⃣ Collect static files en producción
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Recolectando archivos estáticos para producción..."
    python manage.py collectstatic --noinput
fi


# 5️⃣ Arrancar servidor
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Arrancando Gunicorn (producción)..."
    exec gunicorn fishdex.wsgi:application --bind 0.0.0.0:8000 --workers 3 --log-level info
else
    echo "Arrancando Django runserver (desarrollo)..."
    exec python manage.py runserver 0.0.0.0:8000
fi
