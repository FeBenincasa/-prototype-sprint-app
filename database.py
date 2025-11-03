import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import os

# Database setup
DATABASE_URL = "sqlite:///tasks.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False)
    due_date = Column(Date, nullable=True)
    created_at = Column(Date, default=date.today)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def add_task(title, due_date=None):
    """Add a new task"""
    db = SessionLocal()
    try:
        # Parse due_date if provided
        parsed_date = None
        if due_date:
            try:
                parsed_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            except ValueError:
                parsed_date = None
        
        task = Task(title=title, due_date=parsed_date)
        db.add(task)
        db.commit()
        db.refresh(task)
        
        return {
            "id": task.id,
            "title": task.title,
            "done": task.done,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": task.created_at.isoformat()
        }
    except Exception as e:
        db.rollback()
        print(f"Error adding task: {e}")
        return None
    finally:
        db.close()

def get_tasks():
    """Get all tasks"""
    db = SessionLocal()
    try:
        tasks = db.query(Task).all()
        return [
            {
                "id": task.id,
                "title": task.title,
                "done": task.done,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]
    except Exception as e:
        print(f"Error getting tasks: {e}")
        return []
    finally:
        db.close()

def toggle_done(task_id):
    """Toggle task completion status"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.done = not task.done
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"Error toggling task: {e}")
        return False
    finally:
        db.close()

def delete_task(task_id):
    """Delete a task"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"Error deleting task: {e}")
        return False
    finally:
        db.close()

def get_today_tasks():
    """Get tasks due today"""
    db = SessionLocal()
    try:
        today = date.today()
        tasks = db.query(Task).filter(Task.due_date == today, Task.done == False).all()
        return [
            {
                "id": task.id,
                "title": task.title,
                "due_date": task.due_date.isoformat() if task.due_date else None
            }
            for task in tasks
        ]
    except Exception as e:
        print(f"Error getting today's tasks: {e}")
        return []
    finally:
        db.close()

# Initialize database if it doesn't exist
if not os.path.exists("tasks.db"):
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")