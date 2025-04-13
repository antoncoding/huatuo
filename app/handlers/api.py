from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models.database import get_session_maker
from app.config.settings import PORT

class APIServer:
    """Handles FastAPI server operations."""
    
    def __init__(self):
        self.app = FastAPI(
            title="RAG Chatbot API",
            description="A simple RAG-based chatbot API that answers questions based on your documents",
            version="1.0.0"
        )
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup FastAPI routes."""
        @self.app.get("/")
        async def root():
            """Root endpoint with basic information."""
            return {
                "status": "online",
                "message": "RAG Chatbot API is running. Telegram bot is active.",
                "port": PORT
            }
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy"}
    
    def get_app(self):
        """Get the FastAPI application instance."""
        return self.app 