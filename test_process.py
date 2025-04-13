import logging
import sys
from sqlalchemy.orm import Session

from app.models.database import init_db, get_session_maker
from app.services.document_processor import DocumentProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def test_document_processing():
    """Test document processing functionality."""
    try:
        # Initialize database
        logger.info("Initializing database...")
        engine = init_db()
        SessionLocal = get_session_maker(engine)
        db = SessionLocal()
        
        try:
            # Initialize processor
            processor = DocumentProcessor(db)
            
            # Test document processing
            logger.info("Starting document processing test...")
            await processor.process_documents()
            
            logger.info("Document processing test completed successfully!")
            
        except Exception as e:
            logger.error(f"Error during processing: {str(e)}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_document_processing()) 