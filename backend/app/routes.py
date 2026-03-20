from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Budget, BudgetColumn, ExpenseItem
from app.schemas import (
    BudgetResponse,
    BudgetUpdate,
    BudgetColumnCreate,
    BudgetColumnResponse,
    ExpenseItemCreate,
    ExpenseItemResponse,
)

router = APIRouter()


@router.get("/budget", response_model=BudgetResponse)
def get_budget(db: Session = Depends(get_db)):
    budget = db.query(Budget).first()
    if not budget:
        budget = Budget(planned_amount=0)
        db.add(budget)
        db.commit()
        db.refresh(budget)
    return budget


@router.patch("/budget", response_model=BudgetResponse)
def update_budget(data: BudgetUpdate, db: Session = Depends(get_db)):
    budget = db.query(Budget).first()
    if not budget:
        budget = Budget(planned_amount=data.planned_amount)
        db.add(budget)
    else:
        budget.planned_amount = data.planned_amount
    db.commit()
    db.refresh(budget)
    return budget


@router.post("/columns", response_model=BudgetColumnResponse)
def create_column(data: BudgetColumnCreate, db: Session = Depends(get_db)):
    column = BudgetColumn(name=data.name, budget_id=data.budget_id)
    db.add(column)
    db.commit()
    db.refresh(column)
    return column


@router.delete("/columns/{column_id}")
def delete_column(column_id: int, db: Session = Depends(get_db)):
    column = db.query(BudgetColumn).filter(BudgetColumn.id == column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    db.delete(column)
    db.commit()
    return {"message": "Column deleted"}


@router.post("/items", response_model=ExpenseItemResponse)
def create_item(data: ExpenseItemCreate, db: Session = Depends(get_db)):
    item = ExpenseItem(
        title=data.title,
        description=data.description,
        cost=data.cost,
        column_id=data.column_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ExpenseItem).filter(ExpenseItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}
