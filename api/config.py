from dotenv import load_dotenv
from os import getenv

# Load environment variables
load_dotenv()


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_CSS = getenv("SWAGGER_UI_CSS")
    SWAGGER_UI_BUNDLE_JS = getenv("SWAGGER_UI_BUNDLE_JS")
    SWAGGER_UI_STANDALONE_PRESET_JS = getenv("SWAGGER_UI_STANDALONE_PRESET_JS")
    REDOC_STANDALONE_JS = getenv("REDOC_STANDALONE_JS")


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass
