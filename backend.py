from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship, Session, sessionmaker  # Added sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class Priority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(100), nullable=False)
    taskName = Column(String(255), nullable=False)
    taskDetail = Column(Text, nullable=True)
    priority = Column(String(20), nullable=True)
    assignee = Column(String(100), nullable=True)
    createdAt = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updatedAt = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    subtasks = relationship("Subtask", back_populates="task", cascade="all, delete-orphan")

class Subtask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    taskId = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    detail = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    initiated = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updatedAt = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    task = relationship("Task", back_populates="subtasks")

# Database setup and functions
from sqlalchemy import create_engine

engine = create_engine("sqlite:///buraqmanager.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_tasks(db):
    return db.query(Task).all()

def get_task(db, task_id):
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db, category, task_name, task_detail=None, priority=None, assignee=None):
    db_task = Task(category=category, taskName=task_name, taskDetail=task_detail, priority=priority.value if priority else None, assignee=assignee)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db, task_id, category=None, task_name=None, task_detail=None, priority=None, assignee=None):
    db_task = get_task(db, task_id)
    if db_task:
        if category:
            db_task.category = category
        if task_name:
            db_task.taskName = task_name
        if task_detail is not None:
            db_task.taskDetail = task_detail
        if priority:
            db_task.priority = priority.value
        if assignee:
            db_task.assignee = assignee
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db, task_id):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

def create_subtask(db, task_id, name, detail=None, completed=False, initiated=False):
    db_task = get_task(db, task_id)
    if db_task:
        db_subtask = Subtask(taskId=task_id, name=name, detail=detail, completed=completed, initiated=initiated)
        db.add(db_subtask)
        db.commit()
        db.refresh(db_subtask)
        return db_subtask
    return None

def update_subtask(db, subtask_id, name=None, detail=None, completed=None, initiated=None):
    db_subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if db_subtask:
        if name:
            db_subtask.name = name
        if detail is not None:
            db_subtask.detail = detail
        if completed is not None:
            db_subtask.completed = completed
        if initiated is not None:
            db_subtask.initiated = initiated
        db.commit()
        db.refresh(db_subtask)
    return db_subtask

def delete_subtask(db, subtask_id):
    db_subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if db_subtask:
        db.delete(db_subtask)
        db.commit()
        return True
    return False