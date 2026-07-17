
from fastapi import FastAPI, Request
from fastapi.params import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from src.routes import studentrouter
import uvicorn
from src.config.db import Base, engine
from src.models.StudentData import StudentData

app = FastAPI(title ="My FastAPI App", description="A simple FastAPI application with HTML templates", version="1.0.0")
app.include_router(studentrouter.router)
Base.metadata.create_all(bind=engine)


@app.get("/", summary="Root endpoint")
def root():
    return {"message": "Welcome to the API"}
