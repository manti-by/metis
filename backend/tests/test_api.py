import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

import app.database as database_module

database_module.engine = test_engine
database_module.SessionLocal = TestingSessionLocal

from app.main import app
from app.database import Base, get_db


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    return TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Metis API"}


def test_get_budget_creates_new(client):
    response = client.get("/api/budget")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["planned_amount"] == 0
    assert data["columns"] == []


def test_update_budget(client):
    response = client.patch("/api/budget", json={"planned_amount": 1000})
    assert response.status_code == 200
    data = response.json()
    assert data["planned_amount"] == 1000


def test_create_column(client):
    budget_response = client.get("/api/budget")
    budget_id = budget_response.json()["id"]

    response = client.post(
        "/api/columns", json={"name": "Shopping", "budget_id": budget_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Shopping"
    assert data["budget_id"] == budget_id
    assert data["items"] == []


def test_create_and_get_column(client):
    budget_response = client.get("/api/budget")
    budget_id = budget_response.json()["id"]

    client.post("/api/columns", json={"name": "Food", "budget_id": budget_id})

    budget = client.get("/api/budget").json()
    assert len(budget["columns"]) == 1
    assert budget["columns"][0]["name"] == "Food"


def test_delete_column(client):
    budget_response = client.get("/api/budget")
    budget_id = budget_response.json()["id"]

    column_response = client.post(
        "/api/columns", json={"name": "ToDelete", "budget_id": budget_id}
    )
    column_id = column_response.json()["id"]

    response = client.delete(f"/api/columns/{column_id}")
    assert response.status_code == 200

    budget = client.get("/api/budget").json()
    assert len(budget["columns"]) == 0


def test_delete_nonexistent_column(client):
    response = client.delete("/api/columns/999")
    assert response.status_code == 404


def test_create_item(client):
    budget_response = client.get("/api/budget")
    budget_id = budget_response.json()["id"]

    column_response = client.post(
        "/api/columns", json={"name": "Tech", "budget_id": budget_id}
    )
    column_id = column_response.json()["id"]

    response = client.post(
        "/api/items",
        json={
            "title": "Laptop",
            "description": "MacBook Pro",
            "cost": 1999.99,
            "column_id": column_id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Laptop"
    assert data["description"] == "MacBook Pro"
    assert data["cost"] == 1999.99


def test_create_item_updates_column(client):
    budget_response = client.get("/api/budget")
    budget_id = budget_response.json()["id"]

    column_response = client.post(
        "/api/columns", json={"name": "Travel", "budget_id": budget_id}
    )
    column_id = column_response.json()["id"]

    client.post(
        "/api/items", json={"title": "Flight", "cost": 500, "column_id": column_id}
    )

    budget = client.get("/api/budget").json()
    column = budget["columns"][0]
    assert len(column["items"]) == 1
    assert column["items"][0]["title"] == "Flight"


def test_delete_item(client):
    budget_response = client.get("/api/budget")
    budget_id = budget_response.json()["id"]

    column_response = client.post(
        "/api/columns", json={"name": "Books", "budget_id": budget_id}
    )
    column_id = column_response.json()["id"]

    item_response = client.post(
        "/api/items", json={"title": "Novel", "cost": 15, "column_id": column_id}
    )
    item_id = item_response.json()["id"]

    response = client.delete(f"/api/items/{item_id}")
    assert response.status_code == 200

    budget = client.get("/api/budget").json()
    assert len(budget["columns"][0]["items"]) == 0


def test_delete_nonexistent_item(client):
    response = client.delete("/api/items/999")
    assert response.status_code == 404
