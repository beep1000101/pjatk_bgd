from flask import Blueprint, request, jsonify
from sqlalchemy import select

from database.models.orders import Order

from flask_app.app import db
from flask_app.schemas.orders import OrderSchema
from flask_app.routes.errors import APIError
from flask_app.routes.utils.decorators import transactional

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

signle_order_schema = OrderSchema()
multiple_orders_schema = OrderSchema(many=True)


@orders_bp.post("/")
@transactional("Order already exists or violates a constraint.")
def create_order():
    # Expect JSON body with order fields
    data = request.get_json()
    errors = signle_order_schema.validate(data)
    if errors:
        raise APIError(errors, 400)

    new_order = signle_order_schema.load(data)
    db.session.add(new_order)
    db.session.flush()  # Use flush to get ID before commit (commit is handled by decorator)
    db.session.refresh(new_order)
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
@transactional("Order update violates a constraint.")
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
    # No need to call commit, handled by decorator
    return jsonify(signle_order_schema.dump(updated_order)), 200


@orders_bp.delete("/<int:order_id>")
@transactional("Order delete violates a constraint.")
def delete_order(order_id):
    order = db.session.execute(
        select(Order).where(Order.id == order_id)
    ).scalar_one_or_none()
    if order is None:
        raise APIError("Order not found", 404)
    db.session.delete(order)
    # No need to call commit, handled by decorator
    return jsonify({"message": "Order deleted"}), 200
