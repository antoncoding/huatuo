from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from app.config.settings import DATABASE_URL

Base = declarative_base()

class Document(Base):
    """Represents a document in the database."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    
    # Relationship with text chunks
    chunks = relationship("TextChunk", back_populates="document", cascade="all, delete-orphan")

class TextChunk(Base):
    """Represents a chunk of text with its embedding."""
    __tablename__ = "text_chunks"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    embedding = Column(Text, nullable=False)  # Store embeddings as JSON string
    
    # Relationship with document
    document = relationship("Document", back_populates="chunks")

def init_db():
    """Initialize the database and create tables."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    return engine

def get_session_maker(engine):
    """Create a session maker for database operations."""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine) 