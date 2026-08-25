from fastapi import FastAPI

from .database import Base, engine
from . import models
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="A FastAPI backend application to manage personal expenses.",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Expense Tracker API",
        "docs": "/docs"
    }