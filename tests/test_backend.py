import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import Base, Task, Subtask, Priority, create_task, get_task, update_task, delete_task, create_subtask, update_subtask, delete_subtask

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    temp_db_path = tempfile.mktemp(suffix='.db')
    engine = create_engine(f"sqlite:///{temp_db_path}")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()
        os.unlink(temp_db_path)

def test_create_task(temp_db):
    """Test creating a task"""
    task = create_task(temp_db, "Test Category", "Test Task", "Test Detail", Priority.high, "Test Assignee")
    assert task is not None
    assert task.category == "Test Category"
    assert task.taskName == "Test Task"
    assert task.taskDetail == "Test Detail"
    assert task.priority == "high"
    assert task.assignee == "Test Assignee"

def test_get_task(temp_db):
    """Test getting a task"""
    # Create a task first
    created_task = create_task(temp_db, "Test Category", "Test Task")
    
    # Get the task
    task = get_task(temp_db, created_task.id)
    assert task is not None
    assert task.id == created_task.id
    assert task.taskName == "Test Task"

def test_update_task(temp_db):
    """Test updating a task"""
    # Create a task first
    task = create_task(temp_db, "Test Category", "Test Task")
    
    # Update the task
    updated_task = update_task(temp_db, task.id, task_name="Updated Task")
    assert updated_task is not None
    assert updated_task.taskName == "Updated Task"

def test_delete_task(temp_db):
    """Test deleting a task"""
    # Create a task first
    task = create_task(temp_db, "Test Category", "Test Task")
    task_id = task.id
    
    # Delete the task
    result = delete_task(temp_db, task_id)
    assert result is True
    
    # Verify task is deleted
    deleted_task = get_task(temp_db, task_id)
    assert deleted_task is None

def test_create_subtask(temp_db):
    """Test creating a subtask"""
    # Create a parent task first
    parent_task = create_task(temp_db, "Test Category", "Parent Task")
    
    # Create a subtask
    subtask = create_subtask(temp_db, parent_task.id, "Test Subtask", "Test Subtask Detail")
    assert subtask is not None
    assert subtask.taskId == parent_task.id
    assert subtask.name == "Test Subtask"
    assert subtask.detail == "Test Subtask Detail"
    assert subtask.completed is False

def test_update_subtask(temp_db):
    """Test updating a subtask"""
    # Create a parent task and subtask
    parent_task = create_task(temp_db, "Test Category", "Parent Task")
    subtask = create_subtask(temp_db, parent_task.id, "Test Subtask")
    
    # Update the subtask
    updated_subtask = update_subtask(temp_db, subtask.id, name="Updated Subtask", completed=True)
    assert updated_subtask is not None
    assert updated_subtask.name == "Updated Subtask"
    assert updated_subtask.completed is True

def test_delete_subtask(temp_db):
    """Test deleting a subtask"""
    # Create a parent task and subtask
    parent_task = create_task(temp_db, "Test Category", "Parent Task")
    subtask = create_subtask(temp_db, parent_task.id, "Test Subtask")
    subtask_id = subtask.id
    
    # Delete the subtask
    result = delete_subtask(temp_db, subtask_id)
    assert result is True 