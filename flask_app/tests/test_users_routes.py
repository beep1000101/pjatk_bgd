import pytest
import uuid

from flask_app.app import create_app, db
from database.db_seed import seed_data, create_tables

from flask_app.config import TestingConfig


@pytest.fixture(scope='function')
def test_app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.drop_all()
        create_tables(bind=db.session.get_bind())
        seed_data(session=db.session)
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def user_data():
    # Ensure unique email for each test run
    unique_email = f"alice_{uuid.uuid4().hex}@example.com"
    return {"name": "Alice", "email": unique_email, "city": "Wonderland"}


def test_create_user(client, user_data):
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["city"] == user_data["city"]
    assert "id" in data


def test_create_user_missing_fields(client):
    response = client.post("/users", json={"name": "Bob"})
    assert response.status_code == 400
    assert "email" in response.get_json()


def test_get_users(client, user_data):
    # Ensure at least one user exists
    client.post("/users", json=user_data)
    response = client.get("/users")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(u["email"] == user_data["email"] for u in data)


def test_get_user(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == user_id


def test_get_user_not_found(client):
    response = client.get("/users/99999")
    assert response.status_code == 404


def test_update_user(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    update = {"city": "New City"}
    response = client.put(f"/users/{user_id}", json=update)
    assert response.status_code == 200
    assert response.get_json()["city"] == "New City"


def test_update_user_not_found(client):
    response = client.put("/users/99999", json={"city": "Nowhere"})
    assert response.status_code == 404


def test_update_user_invalid(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"email": ""})
    assert response.status_code == 400


def test_delete_user(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "User deleted"
    # Confirm user is gone
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404


def test_delete_user_not_found(client):
    response = client.delete("/users/99999")
    assert response.status_code == 404
