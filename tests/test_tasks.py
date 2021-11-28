from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import DataBase
from app.dependencies import get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False, bind=engine)

DataBase.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app, base_url="http://localhost")

test_task = {
    "name": "test name",
    "description": "test description"
}

updated_task = {
    "name": "test name",
    "description": "test description",
    "is_done": True
}


def test_create_task():
    response = client.post("/tasks/", json=test_task)
    assert response.status_code == 201


def test_read_created_task():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json()[-1]["name"] == test_task["name"]
    assert response.json()[-1]["description"] == test_task["description"]
    assert not response.json()[-1]["is_done"]


def test_update_task():
    response = client.get("/tasks/")
    assert response.status_code == 200

    id = response.json()[-1]["id"]
    response = client.put(f"/tasks/{id}/", json=updated_task)
    assert response.status_code == 204

    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json()[-1]["name"] == updated_task["name"]
    assert response.json()[-1]["description"] == updated_task["description"]
    assert response.json()[-1]["is_done"]


def test_delete_task():
    response = client.get("/tasks/")
    assert response.status_code == 200

    id = response.json()[-1]["id"]
    response = client.delete(f"/tasks/{id}/")
    assert response.status_code == 204


def test_read_tasks_after_delete():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 0
