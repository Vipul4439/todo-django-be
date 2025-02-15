import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
load_dotenv()
# Get DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")


# Create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# Define the ToDo model
class ToDoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic model for request validation
class ToDoItem(BaseModel):
    title: str
    description: str
    completed: bool = False

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new ToDo item
@app.post("/todos/")
def create_todo(item: ToDoItem, db: Session = Depends(get_db)):
    todo = ToDoDB(**item.dict())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"id": todo.id, **item.dict()}

# Get all ToDos
@app.get("/todos/")
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(ToDoDB).all()
    return [{"id": todo.id, "title": todo.title, "description": todo.description, "completed": todo.completed} for todo in todos]

# Get a single ToDo by ID
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return {"id": todo.id, "title": todo.title, "description": todo.description, "completed": todo.completed}

# Update a ToDo item
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, item: ToDoItem, db: Session = Depends(get_db)):
    todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    
    todo.title = item.title
    todo.description = item.description
    todo.completed = item.completed
    db.commit()
    return {"id": todo.id, **item.dict()}

# Delete a ToDo item
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "ToDo item deleted successfully"}

# Run Uvicorn server
import uvicorn
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
