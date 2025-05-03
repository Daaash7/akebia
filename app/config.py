import os

from dotenv import load_dotenv


class Config:

    COOKIE_SECRET: str
    DB_URL: str

    def __init__(self):
        self.load_env()

    def load_env(self):
        load_dotenv()

        self.COOKIE_SECRET = os.environ.get("COOKIE_SECRET")
        self.DB_URL = os.environ.get("DB_URL")


config = Config()