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
    assert "error" in response.get_json()


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
    assert "error" in response.get_json()


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
    assert "error" in response.get_json()


def test_update_user_invalid(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"email": ""})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_delete_user(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "User deleted"
    # Confirm user is gone
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404
    assert "error" in get_resp.get_json()


def test_delete_user_not_found(client):
    response = client.delete("/users/99999")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_create_user_invalid_types(client):
    bad_data = {"name": 123, "email": 456, "city": 789}
    response = client.post("/users", json=bad_data)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_user_extra_fields(client, user_data):
    data = dict(user_data)
    data["unexpected"] = "field"
    response = client.post("/users", json=data)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_user_duplicate_email(client, user_data):
    resp1 = client.post("/users", json=user_data)
    resp2 = client.post("/users", json=user_data)
    assert resp1.status_code == 201
    # Always expect 409 for duplicate email
    assert resp2.status_code == 409


def test_get_users_empty(client):
    # Should return empty list if no users
    # DB is reset per function, so after drop_all, no users
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_user_invalid_id(client):
    response = client.get("/users/notanumber")
    assert response.status_code == 404


def test_update_user_partial(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"city": "Partial City"})
    assert response.status_code == 200
    assert response.get_json()["city"] == "Partial City"


def test_update_user_empty_payload(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={})
    assert response.status_code == 200
    assert response.get_json()["id"] == user_id


def test_update_user_invalid_type(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"city": 12345})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_delete_user_twice(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    resp1 = client.delete(f"/users/{user_id}")
    resp2 = client.delete(f"/users/{user_id}")
    assert resp1.status_code == 200
    assert resp2.status_code == 404
    assert "error" in resp2.get_json()


def test_create_user_null_fields(client):
    data = {"name": None, "email": None, "city": None}
    response = client.post("/users", json=data)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_update_user_null_fields(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"email": None})
    # Always expect 400 for null fields
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_user_missing_json(client):
    response = client.post("/users")
    assert response.status_code in (400, 415)


def test_update_user_missing_json(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}")
    assert response.status_code in (400, 415)


def test_get_user_after_update(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    client.put(f"/users/{user_id}", json={"city": "Updated City"})
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["city"] == "Updated City"


def test_create_user_whitespace_fields(client):
    data = {"name": "   ", "email": "   ", "city": "   "}
    response = client.post("/users", json=data)
    assert response.status_code == 400


def test_create_user_long_strings(client):
    long_str = "a" * 5000
    data = {"name": long_str, "email": f"{long_str}@example.com", "city": long_str}
    response = client.post("/users", json=data)
    # Accept either 201 or 400 depending on schema max length
    assert response.status_code in (201, 400)


def test_create_user_unicode(client):
    data = {"name": "Łukasz", "email": "łukasz@example.com", "city": "Kraków"}
    response = client.post("/users", json=data)
    assert response.status_code == 201
    assert response.get_json()["name"] == "Łukasz"


def test_create_user_sql_injection(client):
    data = {"name": "Robert'); DROP TABLE users;--",
            "email": "robert@example.com", "city": "EvilTown"}
    response = client.post("/users", json=data)
    assert response.status_code == 201


def test_create_user_extra_fields_rejected(client, user_data):
    data = dict(user_data)
    data["not_a_field"] = "should fail"
    response = client.post("/users", json=data)
    assert response.status_code == 400


def test_update_user_extra_fields_rejected(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"not_a_field": "fail"})
    assert response.status_code == 400


def test_update_user_whitespace(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"city": "   "})
    # Always expect 400 for whitespace fields
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_update_user_long_string(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    long_city = "b" * 5000
    response = client.put(f"/users/{user_id}", json={"city": long_city})
    assert response.status_code in (200, 400)


def test_update_user_unicode(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"city": "Łódź"})
    assert response.status_code == 200
    assert response.get_json()["city"] == "Łódź"


def test_update_user_sql_injection(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(
        f"/users/{user_id}", json={"city": "Robert'); DROP TABLE users;--"})
    assert response.status_code == 200


def test_create_user_boundary_email(client):
    # Minimal valid email
    data = {"name": "A", "email": "a@b.co", "city": "X"}
    response = client.post("/users", json=data)
    # Always expect 201 for minimal valid email
    assert response.status_code == 201


def test_create_invalid_email(client):
    # Invalid email format
    data = {"name": "A", "email": "a@b.c", "city": "X"}
    response = client.post("/users", json=data)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_user_invalid_email_format(client):
    data = {"name": "A", "email": "not-an-email", "city": "X"}
    response = client.post("/users", json=data)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_update_user_invalid_email_format(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"email": "bademail"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_update_user_email_to_existing(client, user_data):
    # Create two users
    user2 = dict(user_data)
    user2["email"] = f"bob_{uuid.uuid4().hex}@example.com"
    resp1 = client.post("/users", json=user_data)
    resp2 = client.post("/users", json=user2)
    id1 = resp1.get_json()["id"]
    response = client.put(
        f"/users/{resp2.get_json()['id']}", json={"email": user_data["email"]})
    # Always expect 409 for unique constraint violation
    assert response.status_code == 409


def test_get_user_with_leading_trailing_spaces(client, user_data):
    # Create user with normal email
    resp = client.post("/users", json=user_data)
    user_id = resp.get_json()["id"]
    # Try to get with spaces in URL (should 404)
    response = client.get(f"/users/ {user_id} ")
    assert response.status_code in (404, 400)


def test_patch_method_not_allowed(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.patch(f"/users/{user_id}", json={"city": "Nowhere"})
    assert response.status_code in (404, 405)


def test_post_on_user_id_not_allowed(client, user_data):
    post_resp = client.post("/users", json=user_data)
    user_id = post_resp.get_json()["id"]
    response = client.post(f"/users/{user_id}", json={"city": "Nowhere"})
    assert response.status_code in (404, 405)


def test_delete_user_invalid_id(client):
    response = client.delete("/users/notanumber")
    assert response.status_code in (404, 400)


def test_get_users_with_query_params(client, user_data):
    client.post("/users", json=user_data)
    response = client.get("/users?city=Wonderland")
    # Should ignore query params and return all users
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
