# ALLSettings.py

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # API keys
    @property
    def API_KEY(self):
        return os.getenv('API_KEY')

    @property
    def SECRET_KEY(self):
        return os.getenv('SECRET_KEY')

    # Database
    @property
    def DB_HOST(self):
        return os.getenv('DB_HOST')

    @property
    def DB_NAME(self):
        return os.getenv('DB_NAME')

    # Risk limits
    @property
    def MAX_DRAWDOWN(self):
        return float(os.getenv('MAX_DRAWDOWN'))

    @property
    def MAX_POSITION_SIZE(self):
        return float(os.getenv('MAX_POSITION_SIZE'))

    # Load .env
    def __init__(self):
        self.reload()

    def reload(self):
        load_dotenv()


settings = Settings()