import pytest
import os
os.environ["TESTING"] = "1"
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_students(client):
    # Ensure there is at least one student
    created = client.post("/api/students", json={"name": "Тестовый Студент"})
    assert created.status_code == 201

    resp = client.get("/api/students")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert any("name" in s for s in data)

def test_add_student(client):
    new_student = {"name": "Мария Кузнецова"}
    resp = client.post("/api/students", json=new_student)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == new_student["name"]

    # проверим, что студент появился
    resp2 = client.get("/api/students")
    students = resp2.get_json()
    assert any(s["name"] == "Мария Кузнецова" for s in students)

def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"
    assert "db" in data