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


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = getenv("DEV_DATABASE_URL")


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = getenv("TEST_DATABASE_URL")
    TESTING = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = getenv("PROD_DATABASE_URI")
    BCRYPT_LOG_ROUNDS = 12


config_dict = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
}
