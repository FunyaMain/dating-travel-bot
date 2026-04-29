import os
from dotenv import load_dotenv

load_dotenv()


# 🤖 BOT
BOT_TOKEN = os.getenv("BOT_TOKEN")


# 👑 Админ (если используешь)
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


# 📢 Канал / чат
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHAT_ID = os.getenv("CHAT_ID")


# 🗄 База данных (Railway)
DATABASE_URL = os.getenv("DATABASE_URL")


# 🛠 АДМИН-ЛОГ (ДОБАВЛЕНО)
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))
ADMIN_TOPIC_ID = int(os.getenv("ADMIN_TOPIC_ID", "0"))
