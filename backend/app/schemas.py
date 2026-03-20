from typing import Optional

from pydantic import BaseModel, ConfigDict


class ExpenseItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    cost: float
    column_id: int


class ExpenseItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str]
    cost: float
    column_id: int


class BudgetColumnCreate(BaseModel):
    name: str
    budget_id: int


class BudgetColumnResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    budget_id: int
    items: list[ExpenseItemResponse] = []


class BudgetUpdate(BaseModel):
    planned_amount: float


class BudgetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    planned_amount: float
    columns: list[BudgetColumnResponse] = []
