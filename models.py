from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    chunks = relationship("TextChunk", back_populates="document", cascade="all, delete-orphan")

class TextChunk(Base):
    __tablename__ = 'text_chunks'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    document_id = Column(Integer, ForeignKey('documents.id'))
    embedding = Column(Text)  # Store embedding as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    document = relationship("Document", back_populates="chunks")

# Database initialization
def init_db():
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    engine = create_engine(database_url or 'postgresql://localhost/ragbot')
    Base.metadata.create_all(engine)
    return engine 