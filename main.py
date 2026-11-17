from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Task Manager API")

# 1. Define the Task Data Model using Pydantic
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    category: str = "General"  # e.g., "Study", "Work", "Personal"
    is_completed: bool = False

# 2. In-memory temporary database (a simple Python list for now)
tasks_db: List[Task] = [
    Task(id=1, title="Learn FastAPI", description="Set up first API endpoints", category="Study", is_completed=True),
    Task(id=2, title="Build JavaScript Frontend", description="Connect to backend API", category="Coding", is_completed=False),
]

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API!"}

# GET all tasks
@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    return tasks_db

# POST a new task
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    # Auto-generate a new ID
    new_id = len(tasks_db) + 1 if tasks_db else 1
    task.id = new_id
    tasks_db.append(task)
    return task