import os
import logging
from typing import List
from sqlalchemy.orm import Session
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.schema import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.models.database import Document
from app.config.settings import TEXT_DIRECTORY

# Define vector store path
VECTOR_STORE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge")

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document processing and vector store creation."""
    
    def __init__(self, db: Session):
        self.db = db
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Reduced chunk size
            chunk_overlap=200,  # Reduced overlap
            separators=["\n\n\n", "\n\n", "\n", "。", "！", "？", " ", ""]
        )
        self.vector_store = None
    
    def _print_chunk_sample(self, chunk: str, chunk_num: int):
        """Print a formatted chunk sample with clear boundaries."""
        logger.info(f"\n{'='*80}\nCHUNK #{chunk_num}:\n{'-'*80}\n{chunk}\n{'='*80}\n")
    
    async def process_documents(self) -> FAISS:
        """Process documents and create vector store.
        
        Returns:
            FAISS: The created vector store
        """
        if not os.path.exists(TEXT_DIRECTORY):
            logger.warning(f"Directory {TEXT_DIRECTORY} does not exist. Creating it...")
            os.makedirs(TEXT_DIRECTORY)
        
        # Load documents
        logger.info("Loading documents...")
        loader = DirectoryLoader(
            TEXT_DIRECTORY,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents")
        
        # Initialize vector store with first document
        if not documents:
            logger.warning("No documents found to process!")
            return None
            
        logger.info("Processing first document to initialize vector store...")
        first_doc = documents[0]
        first_splits = self.text_splitter.split_text(first_doc.page_content)
        first_docs = [LangchainDocument(page_content=text) for text in first_splits]
        self.vector_store = FAISS.from_documents(
            documents=first_docs,
            embedding=self.embeddings
        )
        logger.info(f"Initialized vector store with {len(first_splits)} chunks from first document")
        
        # Process remaining documents in batches
        batch_size = 5  # Process 5 documents at a time
        for i in range(1, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            logger.info(f"Processing batch of {len(batch)} documents...")
            
            for doc in batch:
                try:
                    # Split document into chunks
                    splits = self.text_splitter.split_text(doc.page_content)
                    logger.info(f"Split document into {len(splits)} chunks")
                    
                    # Convert chunks to Document objects
                    doc_chunks = [LangchainDocument(page_content=text) for text in splits]
                    
                    # Add chunks to vector store
                    self.vector_store.add_documents(doc_chunks)
                    logger.info(f"Added {len(splits)} chunks to vector store")
                    
                except Exception as e:
                    logger.error(f"Error processing document: {str(e)}")
                    continue
        
        logger.info(f"Final vector store contains {self.vector_store.index.ntotal} chunks")
        
        # Save vector store to disk
        if not os.path.exists(VECTOR_STORE_PATH):
            os.makedirs(VECTOR_STORE_PATH)
        self.vector_store.save_local(VECTOR_STORE_PATH)
        logger.info(f"Vector store saved to {VECTOR_STORE_PATH}")
        
        logger.info("Document processing completed successfully!")
        return self.vector_store 