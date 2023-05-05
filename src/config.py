"""Flask configuration."""
from __future__ import annotations

from os import environ, path

from dotenv import load_dotenv

base_path = path.dirname(__file__)
basedir = path.abspath(base_path)
env_path = path.join(basedir, ".env")

load_dotenv(env_path)

AVAILABLE_ENVIRONMENTS = ["development", "production"]


class ConfigException(Exception):
    pass


class AppyConfig:
    """Base config."""

    environ = {
        key: value.strip().replace("'", "").replace('"', "")
        for key, value in environ.items()
    }

    APP_PORT = environ.get("APP_PORT")
    APP_HOST = environ.get("APP_HOST") or "localhost"
    SECRET_KEY = environ.get("SECRET_KEY") or "12345"
    FLASK_ENV = (
        environ.get("FLASK_ENV").strip()
        if isinstance(environ.get("FLASK_ENV"), str)
        else "development"
    )

    DATABASE_ENGINE = environ.get("DATABASE_ENGINE")
    DATABASE_USERNAME = environ.get("DATABASE_USERNAME")
    DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
    DATABASE_HOST = environ.get("DATABASE_HOST")
    DATABASE_NAME = environ.get("DATABASE_NAME")
    DATABASE_PORT = environ.get("DATABASE_PORT")

    DATABASE_URI_str = "{engine}://{username}:{password}@{host}:{port}/{name}"

    DATABASE_URI = DATABASE_URI_str.format(
        engine=DATABASE_ENGINE or "postgresql",
        username=DATABASE_USERNAME or "postgres",
        password=DATABASE_PASSWORD or "postgres",
        host=DATABASE_HOST or "localhost",
        name=DATABASE_NAME or "appy_db",
        port=DATABASE_PORT or "5432",
    )

    env_flag = FLASK_ENV == "development"

    DEBUG = env_flag
    TESTING = env_flag

    def toDict(self):
        return self.__dict__()

    def __dict__(self):
        return {
            "DATABASE_URI": self.DATABASE_URI,
            "APP_PORT": self.APP_PORT,
            "APP_HOST": self.APP_HOST,
            "SECRET_KEY": self.SECRET_KEY,
            "FLASK_ENV": self.FLASK_ENV,
            "DEBUG": self.DEBUG,
            "TESTING": self.TESTING,
        }
