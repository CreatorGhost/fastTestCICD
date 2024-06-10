from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()  

app = FastAPI()

# Sample data from .env for demonstration
SAMPLE_DATA = os.getenv("SAMPLE_DATA")

# Pydantic models for request body
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# In-memory storage for simplicity
items = {}

# just a comment
@app.get("/")
def read_root():
    return {"Hello": "World","env":SAMPLE_DATA}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id], "query": q}

@app.post("/items/")
def create_item(item: Item):
    if len(items) >= 10:  # Limiting for simplicity
        raise HTTPException(status_code=400, detail="Item limit reached")
    items[len(items) + 1] = item.dict()
    return items[len(items)]

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item.dict()
    return {"item": items[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"detail": "Item deleted"}
