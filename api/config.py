from dotenv import load_dotenv
from os import getenv

# Load environment variables
load_dotenv()


class BaseConfig:
    # Database Config
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API Docs
    SWAGGER_UI_CSS = getenv("SWAGGER_UI_CSS")
    SWAGGER_UI_BUNDLE_JS = getenv("SWAGGER_UI_BUNDLE_JS")
    SWAGGER_UI_STANDALONE_PRESET_JS = getenv("SWAGGER_UI_STANDALONE_PRESET_JS")
    REDOC_STANDALONE_JS = getenv("REDOC_STANDALONE_JS")

    # Security & Encryption
    SECRET_KEY = getenv("SECRET_KEY")
    BCRYPT_LOG_ROUNDS = 5

    # Email Configurations
    MAIL_SERVER = getenv("MAIL_SERVER")
    MAIL_PORT = getenv("MAIL_PORT")
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = getenv("DEV_DATABASE_URL")


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = getenv("TEST_DATABASE_URL")
    TESTING = True


class ProductionConfig(BaseConfig):
    BCRYPT_LOG_ROUNDS = 12
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )


config_dict = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
}
