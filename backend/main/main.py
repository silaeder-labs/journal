import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import get_test as gt
import os

app = FastAPI()

base_path = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.abspath(os.path.join(base_path, "..", "..", "frontend"))

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/statistic")
def get_statistic_page():
    html_file = os.path.join(frontend_path, "subjects", "statistic", "index.html")
    return FileResponse(html_file)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
def hello():
    return {"message": "Привет от FastAPI 🚀"}

class TextIn(BaseModel):
    text: str

@app.post("/api/user_marks")
def reverse_text(data: TextIn):
    return {"result": gt.get_results_by_user_id(data.text)} #af73452e-bbbb-443d-83a2-423f78cd003e

@app.get("/api/columns")
def get_columns():
    return gt.get_columns_in_database()
