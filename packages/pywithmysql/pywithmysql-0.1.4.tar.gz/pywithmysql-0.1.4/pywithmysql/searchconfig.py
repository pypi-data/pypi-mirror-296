import os
from dotenv import load_dotenv


def get_or_create_config():
    load_dotenv(dotenv_path="config")
    files = os.listdir(".")
    if "config" in files:
        mydata = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "db_name": os.getenv("DB_NAME")
        }
        return mydata


