import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

# For serverless environments, use /tmp directory for SQLite
# This is not a permanent solution but will help diagnose if this is the issue
if os.environ.get('VERCEL'):
    DATABASE_URL = 'sqlite:////tmp/conversations.db'
else:
    DATABASE_URL = 'sqlite:///conversations.db'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(String(36), primary_key=True)
    username = Column(String(50))
    model = Column(String(50))
    start_timestamp = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(36), ForeignKey('conversations.id'))
    role = Column(String(50))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", backref="messages")

def init_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)