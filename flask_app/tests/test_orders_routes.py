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


def test_update_order_invalid(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    # Send invalid data: missing required field
    response = client.put(f"/orders/{order_id}", json={"customer_id": None})
    assert response.status_code == 400


def test_delete_order(client, order_data):
    post_resp = client.post("/orders/", json=order_data)
    order_id = post_resp.get_json()["id"]
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Order deleted"
    get_resp = client.get(f"/orders/{order_id}")
    assert get_resp.status_code == 404


def test_delete_order_not_found(client):
    response = client.delete("/orders/99999")
    assert response.status_code == 404
