import logging
import uvicorn
from sqlalchemy.orm import Session
import signal
import sys
import os
import threading
import atexit

from app.config.settings import PORT, TELEGRAM_TOKEN
from app.models.database import init_db, get_session_maker
from app.handlers.api import APIServer
from app.handlers.telegram import setup_handlers
from app.services.chat_service import ChatService
from telegram.ext import Application

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def run():
    """Run the application."""
    try:
        # Initialize database
        logger.info("Initializing database...")
        engine = init_db()
        SessionLocal = get_session_maker(engine)
        db = SessionLocal()
        
        # Initialize ChatService
        logger.info("Initializing ChatService...")
        chat_service = ChatService()
        
        # Initialize FastAPI server
        logger.info("Initializing FastAPI server...")
        api_server = APIServer()
        app = api_server.get_app()
        
        # Start FastAPI server in a separate thread
        fastapi_thread = threading.Thread(
            target=lambda: uvicorn.run(app, host="0.0.0.0", port=PORT)
        )
        fastapi_thread.daemon = True
        fastapi_thread.start()
        
        # Initialize and run Telegram bot
        logger.info("Initializing Telegram bot...")
        if not TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN environment variable is not set")
        
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        setup_handlers(application, db, chat_service)
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Error during application startup: {str(e)}")
        raise

def cleanup():
    """Cleanup function to be called on exit."""
    logger.info("Cleaning up...")
    # Add any cleanup code here if needed

# Register cleanup function
atexit.register(cleanup)

if __name__ == "__main__":
    run() 