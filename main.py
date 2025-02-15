import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to MongoDB Atlas
client = MongoClient(DATABASE_URL)
db = client.todo_db  # Database name
todo_collection = db.todos  # Collection name

app = FastAPI()

# Pydantic model for request validation
class ToDoItem(BaseModel):
    title: str
    description: str
    completed: bool = False

# Create a new ToDo item
@app.post("/todos/")
def create_todo(item: ToDoItem):
    todo = item.dict()
    result = todo_collection.insert_one(todo)
    return {"id": str(result.inserted_id), **todo}

# Get all ToDos
@app.get("/todos/")
def get_todos():
    todos = list(todo_collection.find())
    return [{"id": str(todo["_id"]), "title": todo["title"], "description": todo["description"], "completed": todo["completed"]} for todo in todos]

# Get a single ToDo by ID
@app.get("/todos/{todo_id}")
def get_todo(todo_id: str):
    todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return {"id": str(todo["_id"]), "title": todo["title"], "description": todo["description"], "completed": todo["completed"]}

# Update a ToDo item
@app.put("/todos/{todo_id}")
def update_todo(todo_id: str, item: ToDoItem):
    result = todo_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": item.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return {"id": todo_id, **item.dict()}

# Delete a ToDo item
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    result = todo_collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return {"message": "ToDo item deleted successfully"}

# Run Uvicorn server
import uvicorn
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
