from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    planned_amount = Column(Float, default=0)
    columns = relationship(
        "BudgetColumn", back_populates="budget", cascade="all, delete-orphan"
    )


class BudgetColumn(Base):
    __tablename__ = "budget_columns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    budget = relationship("Budget", back_populates="columns")
    items = relationship(
        "ExpenseItem", back_populates="column", cascade="all, delete-orphan"
    )


class ExpenseItem(Base):
    __tablename__ = "expense_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    cost = Column(Float, nullable=False)
    column_id = Column(Integer, ForeignKey("budget_columns.id"), nullable=False)
    column = relationship("BudgetColumn", back_populates="items")
