import os
from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings

# Detecta entorno, ejemplo: development, staging, production
ENV = os.getenv("DJANGO_ENV", "development")


class ServiceSettings(BaseSettings):
    django_api_url: str = ""
    debug: bool = False

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: str | bool) -> bool:
        """Convierte valores tipo string a booleano."""
        if isinstance(value, bool):
            return value
        return str(value).lower() in {"1", "true", "yes", "on"}

    # ✅ Configuración moderna para Pydantic v2

    model_config = ConfigDict(  # type: ignore
        env_file=f".env.{ENV}",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignora variables extras en el .env
    )


# Crear instancia de configuración
settings = ServiceSettings()
