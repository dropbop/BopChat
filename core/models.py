import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

# For a small app, we use a SQLite database.
DATABASE_URL = 'sqlite:///conversations.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(String(36), primary_key=True)  # Changed to String(36) and primary_key
    username = Column(String(50))
    model = Column(String(50)) # Added model column to store which model was used
    start_timestamp = Column(DateTime, default=datetime.utcnow) # Renamed to start_timestamp

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True) # Integer, primary key, autoincrement
    conversation_id = Column(String(36), ForeignKey('conversations.id')) # ForeignKey to conversations.id
    role = Column(String(50)) # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", backref="messages") # Relationship for easier access

def init_db():
    Base.metadata.create_all(bind=engine)