import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
IMAGES_TEMP_DIR = f"{BASE_DIR}/images_temp"

PROJECT_NAME = os.getenv("PROJECT_NAME", "weather_telegram_bot")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEATHER_TOKEN =os.getenv("WEATHER_TOKEN")
MAX_BUTTON_TEXT_LENGTH = int(os.getenv("MAX_BUTTON_TEXT_LENGTH", 60))
MAX_MESSAGE_TEXT_LENGTH = int(os.getenv("MAX_MESSAGE_TEXT_LENGTH", 4096))