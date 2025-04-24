import os

from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_ASYNC_DRIVER = os.getenv("DB_ASYNC_DRIVER")

    @property
    def async_db_url(self):
        return f"postgresql+{self.DB_ASYNC_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
