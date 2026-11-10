
import os
from pathlib import Path

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# Load environment variables from the project folder.
PROJECT_DIR = Path(__file__).resolve().parent
ENV_FILE = PROJECT_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE)


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            connection_timeout=5
        )

        if connection.is_connected():
            print("Successfully connected to airport_management!")
            return connection

    except (Error, ValueError) as e:
        print(f"Database connection failed: {e}")

    return None
