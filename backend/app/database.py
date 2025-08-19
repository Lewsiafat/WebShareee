import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define the path to the database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'web_hosting.db')}"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()

# Define the Page model
class Page(Base):
    __tablename__ = "pages"

    id = Column(String(10), primary_key=True, index=True)
    title = Column(String(200), nullable=True)
    html_content = Column(Text, nullable=True) # Store HTML content directly for code uploads
    file_path = Column(String(500), nullable=True) # Path to the HTML file on disk
    created_at = Column(DateTime, default=datetime.now)
    view_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

# Define the Asset model
class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(String(10), index=True)
    file_name = Column(String(255))
    file_type = Column(String(50))
    file_path = Column(String(500))
    uploaded_at = Column(DateTime, default=datetime.now)

# Function to create all tables
def create_db_and_tables():
    Base.metadata.create_all(engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
