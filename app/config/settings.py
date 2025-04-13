import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application settings
PORT = int(os.getenv("PORT", 8000))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Admin configuration
ADMIN_USER_IDS = [int(id) for id in os.getenv("ADMIN_USER_IDS", "").split(",") if id]

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rag_chatbot.db")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Document processing settings
TEXT_DIRECTORY = "text_files"
