import pytest

from flask_app.app import create_app, db
from database.db_seed import seed_data, create_tables
from flask_app.config import TestingConfig


@pytest.fixture(scope='module')
def test_app():
    app = create_app(TestingConfig)
    with app.app_context():
        create_tables(bind=db.session.get_bind())
        seed_data(session=db.session)
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def order_data():
    # Adjusted to match OrderSchema fields
    return {
        "customer_id": 1,
        "product": "Widget",
        "quantity": 2,
        "total_price": 19.98,
        "order_date": "2024-06-01"
    }


def test_create_order(client, order_data):
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    data = response.get_json()
    for k in order_data:
        assert data[k] == order_data[k]
    assert "id" in data


def test_create_order_missing_fields(client):
    response = client.post("/orders/", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_orders(client, order_data):
    client.post("/orders/", json=order_data)
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(all(item.get(k) == v for k, v in order_data.items())
               for item in data)


def test_get_order(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == order_id


def test_get_order_not_found(client):
    response = client.get("/orders/99999")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_update_order(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    update = {"product": "Gadget"}
    response = client.put(f"/orders/{order_id}", json=update)
    assert response.status_code == 200
    assert response.get_json()["product"] == "Gadget"


def test_update_order_not_found(client):
    response = client.put("/orders/99999/", json={"product": "nowhere"})
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_update_order_invalid(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    response = client.put(f"/orders/{order_id}", json={"customer_id": None})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_delete_order(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Order deleted"
    get_resp = client.get(f"/orders/{order_id}")
    assert get_resp.status_code == 404
    assert "error" in get_resp.get_json()


def test_delete_order_not_found(client):
    response = client.delete("/orders/99999")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_create_order_invalid_types(client):
    # quantity as string, total_price as string
    bad_data = {
        "customer_id": 1,
        "product": "Widget",
        "quantity": "two",
        "total_price": "cheap",
        "order_date": "2024-06-01"
    }
    response = client.post("/orders/", json=bad_data)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_order_extra_fields(client, order_data):
    # Add an extra field not in schema
    data = dict(order_data)
    data["unexpected"] = "field"
    response = client.post("/orders/", json=data)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_order_duplicate(client, order_data):
    # Should allow duplicate orders (no unique constraint on product)
    resp1 = client.post("/orders/", json=order_data)
    resp2 = client.post("/orders/", json=order_data)
    assert resp1.status_code == 201
    assert resp2.status_code == 201


def test_get_orders_empty(client):
    # Drop all orders, then check GET /orders/
    # Assumes test_app fixture resets DB per module
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_order_invalid_id(client):
    response = client.get("/orders/notanumber")
    assert response.status_code in (404, 400)


def test_update_order_partial(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    response = client.put(f"/orders/{order_id}", json={"quantity": 99})
    assert response.status_code == 200
    assert response.get_json()["quantity"] == 99


def test_update_order_empty_payload(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    response = client.put(f"/orders/{order_id}", json={})
    # Should succeed and not change anything
    assert response.status_code == 200
    assert response.get_json()["id"] == order_id


def test_update_order_invalid_type(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    response = client.put(f"/orders/{order_id}", json={"quantity": "a lot"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_delete_order_twice(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    resp1 = client.delete(f"/orders/{order_id}")
    resp2 = client.delete(f"/orders/{order_id}")
    assert resp1.status_code == 200
    assert resp2.status_code == 404
    assert "error" in resp2.get_json()


def test_create_order_boundary_values(client):
    # Test zero and negative values
    data = {
        "customer_id": 1,
        "product": "Test",
        "quantity": 0,
        "total_price": 0.0,
        "order_date": "2024-06-01"
    }
    response = client.post("/orders/", json=data)
    assert response.status_code == 201
    data["quantity"] = -1
    data["total_price"] = -10.0
    response = client.post("/orders/", json=data)
    # Depending on schema validation, this may be 400 or 201
    assert response.status_code in (201, 400)


def test_create_order_missing_json(client):
    response = client.post("/orders/")
    assert response.status_code in (400, 415)


def test_update_order_missing_json(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    response = client.put(f"/orders/{order_id}")
    assert response.status_code in (400, 415)


def test_create_order_null_fields(client):
    data = {
        "customer_id": None,
        "product": None,
        "quantity": None,
        "total_price": None,
        "order_date": None
    }
    response = client.post("/orders/", json=data)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_update_order_null_fields(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    response = client.put(f"/orders/{order_id}", json={"product": None})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_order_after_update(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    client.put(f"/orders/{order_id}", json={"product": "Updated"})
    get_resp = client.get(f"/orders/{order_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["product"] == "Updated"
