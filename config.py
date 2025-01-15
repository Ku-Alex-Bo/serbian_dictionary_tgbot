import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = os.getenv("DB_PATH", "project.db")
