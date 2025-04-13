import logging
from telegram import Update
import telegramify_markdown
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sqlalchemy.orm import Session

from app.config.settings import ADMIN_USER_IDS
from app.services.document_processor import DocumentProcessor
from app.services.chat_service import ChatService

logger = logging.getLogger(__name__)

def setup_handlers(application: Application, db: Session, chat_service: ChatService):
    """Setup all Telegram bot handlers."""
    # Initialize processor
    processor = DocumentProcessor(db)
    
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Hello! I'm your RAG-powered assistant. Ask me any question about your documents!\n"
            "Use /help to see available commands."
        )
    
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "Available commands:\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/status - Check bot status\n"
        )
        if update.effective_user.id in ADMIN_USER_IDS:
            help_text += "/process - Process documents (admin only)\n"
        await update.message.reply_text(help_text)
    
    async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        status = "🟢 Bot is running"
        if not chat_service.vector_store:
            status += "\n⚠️ Documents not processed yet"
        else:
            status += "\n✅ Documents processed and ready"
        await update.message.reply_text(status)
    
    async def process_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_USER_IDS:
            await update.message.reply_text("❌ This command is only available for admins.")
            return
        
        await update.message.reply_text("🔄 Starting document processing...")
        
        try:
            vector_store = await processor.process_documents()
            if vector_store:
                await chat_service.set_vector_store(vector_store)
                await update.message.reply_text("✅ Document processing completed successfully!")
                logger.info("System initialization complete!")
            else:
                await update.message.reply_text("⚠️ No documents were processed, but the system is still operational.")
                logger.warning("No documents were processed")
        except Exception as e:
            logger.error(f"Error during processing: {str(e)}")
            await update.message.reply_text(
                "⚠️ There was an error processing documents, but the system is still operational. "
                "You can try processing again later."
            )
    
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            question = update.message.text
            user_id = update.effective_user.id
            logger.info(f"Received Telegram query: {question}")
            
            result = await chat_service.answer_question(user_id, question)
            result_markdown_tgv2 = telegramify_markdown.markdownify(result)
            await update.message.reply_markdown_v2(result_markdown_tgv2)
            logger.info("Query processed and response sent successfully")
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            await update.message.reply_text(
                "I'm having trouble processing your question right now. Please try again later."
            )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("process", process_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) 