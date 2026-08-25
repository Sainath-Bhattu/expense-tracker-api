from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Float, Integer, String

from .database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    expense_date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)