import axios from 'axios';
import type { Budget, CreateItemData, CreateColumnData, BudgetColumn, ExpenseItem } from '../types';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const getBudget = () => api.get<Budget>('/budget').then(res => res.data);

export const updateBudget = (planned_amount: number) =>
  api.patch<Budget>('/budget', { planned_amount }).then(res => res.data);

export const createColumn = (data: CreateColumnData) =>
  api.post<BudgetColumn>('/columns', data).then(res => res.data);

export const deleteColumn = (columnId: number) =>
  api.delete(`/columns/${columnId}`);

export const createItem = (data: CreateItemData) =>
  api.post<ExpenseItem>('/items', data).then(res => res.data);

export const deleteItem = (itemId: number) =>
  api.delete(`/items/${itemId}`);
