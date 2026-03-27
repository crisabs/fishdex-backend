#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
"""

import os
import sys


def get_runtime_environment() -> str:
    """Prefer production automatically on Render when DJANGO_ENV is unset."""
    return os.getenv("DJANGO_ENV") or (
        "production" if os.getenv("RENDER", "").lower() == "true" else "development"
    )


def main():
    """Run administrative tasks."""

    # Detect environment
    env = get_runtime_environment()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"fishdex.settings.{env}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and "
            "available on your PYTHONPATH environment variable. Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
