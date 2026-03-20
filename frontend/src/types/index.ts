export interface ExpenseItem {
  id: number;
  title: string;
  description: string | null;
  cost: number;
  column_id: number;
}

export interface BudgetColumn {
  id: number;
  name: string;
  budget_id: number;
  items: ExpenseItem[];
}

export interface Budget {
  id: number;
  planned_amount: number;
  columns: BudgetColumn[];
}

export interface CreateItemData {
  title: string;
  description?: string;
  cost: number;
  column_id: number;
}

export interface CreateColumnData {
  name: string;
  budget_id: number;
}
