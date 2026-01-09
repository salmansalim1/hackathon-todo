"""
Database initialization script
Creates all tables in Neon PostgreSQL database
"""
from sqlmodel import SQLModel
from database import engine
from models import User, Task

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("✅ Database tables created successfully!")
    print("Tables created: users, tasks")

if __name__ == "__main__":
    init_db()
