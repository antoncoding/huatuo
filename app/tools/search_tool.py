import os
import logging
from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Configure logging
logger = logging.getLogger(__name__)

# Define vector store path
VECTOR_STORE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge")

def init_vector_store():
    """Initialize the vector store from disk."""
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        vector_store = FAISS.load_local(
            VECTOR_STORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        logger.info("Vector store initialized successfully")
        return vector_store
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {str(e)}")
        raise

# Initialize vector store at module level
vector_store = init_vector_store()

@tool
def search_documents(query: str) -> str:
    """Search for relevant documents in Chinese Traditional Medicine.
    
    Args:
        query: The search query：e.g: 熱、寒、咳嗽、頭痛穴道
        
    Returns:
        str: The relevant document content
    """
    try:
        logger.info(f"🔍 Searching documents for query: {query}")
        
        # Retrieve relevant documents
        docs = vector_store.similarity_search(query, k=8)
        if not docs or not docs[0].page_content.strip():
            logger.warning(f"❌ No relevant documents found for query: {query}")
            return "I couldn't find any relevant information in the documents for your query."
        
        # Log the found documents
        logger.info(f"✅ Found {len(docs)} relevant documents:")
        for i, doc in enumerate(docs, 1):
            content_preview = doc.page_content[:100].replace('\n', ' ')
            logger.info(f"   {i}. {content_preview}...")
        
        return "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        logger.error(f"❌ Error searching documents: {str(e)}")
        return "I encountered an error while searching the documents." 