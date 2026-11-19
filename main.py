from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Task Manager API")

# 1. Task Data Model
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    category: str = "General"
    is_completed: bool = False

# Model for updating tasks (all fields optional)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_completed: Optional[bool] = None

# In-memory database
tasks_db: List[Task] = [
    Task(id=1, title="Learn FastAPI", description="Set up first API endpoints", category="Study", is_completed=True),
    Task(id=2, title="Build JavaScript Frontend", description="Connect to backend API", category="Coding", is_completed=False),
]

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
    new_id = max([t.id for t in tasks_db], default=0) + 1
    task.id = new_id
    tasks_db.append(task)
    return task

# PUT: Update an existing task by ID (Day 3)
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_data: TaskUpdate):
    for task in tasks_db:
        if task.id == task_id:
            # Update only fields that were provided
            if updated_data.title is not None:
                task.title = updated_data.title
            if updated_data.description is not None:
                task.description = updated_data.description
            if updated_data.category is not None:
                task.category = updated_data.category
            if updated_data.is_completed is not None:
                task.is_completed = updated_data.is_completed
            return task
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

# DELETE: Remove a task by ID (Day 3)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            deleted_task = tasks_db.pop(index)
            return {"message": f"Task '{deleted_task.title}' successfully deleted", "id": task_id}
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")