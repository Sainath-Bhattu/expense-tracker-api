# Expense Tracker API

A RESTful backend application built with FastAPI to manage personal expenses.

## Features

- Create an expense
- View all expenses
- Filter expenses by category
- Update an expense
- Delete an expense
- View total expense count and total amount
- Interactive API documentation using Swagger UI

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Run the Application

```bash
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001