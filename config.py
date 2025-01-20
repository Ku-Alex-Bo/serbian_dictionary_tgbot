import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = os.getenv("DB_PATH", "project.db")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, 'images')

def get_image_path(folder: str, name: str):
    return os.path.join(IMAGE_FOLDER, folder, name)
