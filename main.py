from fastapi import FastAPI

app = FastAPI(title="Task Manager API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}