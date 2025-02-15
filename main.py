from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()

todo_db = {}

todo_id_counter = 1


class ToDoItem(BaseModel):
    title: str
    description: str
    completed: bool = False


@app.post("/todos/")
def create_todo(item: ToDoItem):
    global todo_id_counter
    todo_id = str(todo_id_counter)
    todo_db[todo_id] = item.dict()
    todo_id_counter += 1
    return {"id": todo_id, **item.dict()}


@app.get("/todos/", response_model=List[dict])
def get_todos():
    return [{"id": todo_id, **todo} for todo_id, todo in todo_db.items()]


@app.get("/todos/{todo_id}")
def get_todo(todo_id: str):
    if todo_id not in todo_db:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return {"id": todo_id, **todo_db[todo_id]}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: str, item: ToDoItem):
    print("todo_id", todo_id, "item", item, flush=True)
    if todo_id not in todo_db:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    todo_db[todo_id] = item.dict()
    return {"id": todo_id, **item.dict()}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    if todo_id not in todo_db:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    del todo_db[todo_id]
    return {"message": "ToDo item deleted successfully"}
