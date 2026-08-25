from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .database import get_db
from .models import Expense
from .schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(category: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Expense)

    if category:
        query = query.filter(Expense.category == category)

    return query.order_by(Expense.expense_date.desc()).all()


@router.get("/summary")
def get_expense_summary(db: Session = Depends(get_db)):
    total_expenses = db.query(func.count(Expense.id)).scalar()
    total_amount = db.query(func.coalesce(func.sum(Expense.amount), 0)).scalar()

    return {
        "total_expenses": total_expenses,
        "total_amount": round(total_amount, 2)
    }


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    existing_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not existing_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    for field, value in expense.model_dump(exclude_unset=True).items():
        setattr(existing_expense, field, value)

    db.commit()
    db.refresh(existing_expense)
    return existing_expense


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    existing_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not existing_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(existing_expense)
    db.commit()

    return {"message": "Expense deleted successfully"}