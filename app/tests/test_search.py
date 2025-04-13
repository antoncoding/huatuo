import logging
import sys
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from sqlalchemy.orm import Session
from app.models.database import init_db, get_session_maker

# Configure logging
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)

# Define vector store path
VECTOR_STORE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge")

def test_search():
    """Test the vector store search functionality."""
    try:
        # Initialize database
        logger.info("🔄 Initializing database...")
        engine = init_db()
        SessionLocal = get_session_maker(engine)
        db = SessionLocal()
        
        # Initialize embeddings with same model as document processor
        logger.info("🔄 Initializing embeddings...")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        
        # Load vector store
        logger.info("🔄 Loading vector store...")
        vector_store = FAISS.load_local(
            VECTOR_STORE_PATH, 
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        # Test search
        test_queries = [
            "咳嗽",
            "發熱",
            "頭痛",
            "腹瀉"
        ]
        
        for query in test_queries:
            logger.info(f"\n🔍 Testing query: {query}")
            docs = vector_store.similarity_search(query, k=3)
            
            if not docs:
                logger.warning(f"❌ No results found for query: {query}")
                continue
                
            logger.info(f"✅ Found {len(docs)} relevant documents:")
            for i, doc in enumerate(docs, 1):
                content_preview = doc.page_content[:100].replace('\n', ' ')
                logger.info(f"   {i}. {content_preview}...")
        
    except Exception as e:
        logger.error(f"❌ Error during test: {str(e)}")
    finally:
        if 'db' in locals():
            db.close()
            logger.info("✅ Database connection closed")

if __name__ == "__main__":
    test_search() 