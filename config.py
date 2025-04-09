import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN = os.getenv("TOKEN")

BASE_URL = os.getenv("BASE_URL")

REPORT_TIME = "2025-04-09 17:50:00"
DEFAULT_CHAT_IDS = [7146706654, 987654321]