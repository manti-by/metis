# Metis - Budget Planner

A React app with FastAPI backend for planning future expenses. Track your planned spending and organize expense items into customizable columns.

## Tech Stack

- **Frontend**: React 19, TypeScript, Vite, Framer Motion
- **Backend**: FastAPI, SQLAlchemy
- **Database**: PostgreSQL

## Features

- Set planned amount to spend
- Create multiple columns to categorize expenses
- Add items with title, description, and cost to each column
- Real-time total calculation of all items
- Visual indicator when expenses exceed planned budget
- Smooth animations and elegant dark theme design

## Quick Start

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
bun install
bun run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/budget` | Get current budget with all columns and items |
| PATCH | `/api/budget` | Update planned amount |
| POST | `/api/columns` | Create a new column |
| DELETE | `/api/columns/{id}` | Delete a column |
| POST | `/api/items` | Create a new expense item |
| DELETE | `/api/items/{id}` | Delete an expense item |

## Environment

Set `DATABASE_URL` for PostgreSQL connection:

```
DATABASE_URL=postgresql://user:password@localhost:5432/metis
```
