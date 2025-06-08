from flask import Blueprint, request, jsonify
from sqlalchemy import select

from database.models.orders import Order

from flask_app.app import db
from flask_app.schemas.orders import OrderSchema
from flask_app.routes.errors import APIError

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

signle_order_schema = OrderSchema()
multiple_orders_schema = OrderSchema(many=True)


@orders_bp.post("/")
def create_order():
    # Expect JSON body with order fields
    data = request.get_json()
    errors = signle_order_schema.validate(data)
    if errors:
        raise APIError(errors, 400)

    new_order = signle_order_schema.load(data)
    db.session.add(new_order)
    db.session.commit()
    db.session.refresh(new_order)  # Refresh to get the ID and other defaults
    return jsonify(signle_order_schema.dump(new_order)), 201


@orders_bp.get("/")
def get_orders():
    orders_selection_statement = select(Order)
    orders_list = (
        db.session.execute(orders_selection_statement)
        .scalars()
        .all()
    )
    return jsonify(multiple_orders_schema.dump(orders_list)), 200


@orders_bp.get("/<int:order_id>")
def get_order(order_id):
    order = db.session.execute(
        select(Order).where(Order.id == order_id)
    ).scalar_one_or_none()
    if order is None:
        raise APIError("Order not found", 404)
    return jsonify(signle_order_schema.dump(order)), 200


@orders_bp.put("/<int:order_id>")
def update_order(order_id):
    order = db.session.execute(
        select(Order).where(Order.id == order_id)
    ).scalar_one_or_none()
    if order is None:
        raise APIError("Order not found", 404)
    data = request.get_json()
    errors = signle_order_schema.validate(data, partial=True)
    if errors:
        raise APIError(errors, 400)
    updated_order = signle_order_schema.load(
        data, instance=order, partial=True)
    db.session.commit()
    return jsonify(signle_order_schema.dump(updated_order)), 200


@orders_bp.delete("/<int:order_id>")
def delete_order(order_id):
    order = db.session.execute(
        select(Order).where(Order.id == order_id)
    ).scalar_one_or_none()
    if order is None:
        raise APIError("Order not found", 404)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 200
