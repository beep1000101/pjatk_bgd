from flask import Blueprint, request, jsonify

from database.models.orders import Order

from flask_app.app import db
from flask_app.schemas.orders import OrderSchema

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

signle_order_schema = OrderSchema()
multiple_orders_schema = OrderSchema(many=True)


@orders_bp.route("", methods=["POST"])
def create_order():
    # Expect JSON body with order fields
    data = request.get_json()
    errors = signle_order_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    order = Order(**data)
    db.session.add(order)
    db.session.commit()
    return signle_order_schema.jsonify(order), 201


@orders_bp.route("", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return multiple_orders_schema.jsonify(orders), 200


@orders_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return signle_order_schema.jsonify(order), 200


@orders_bp.route("/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    errors = signle_order_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(order, key, value)
    db.session.commit()
    return signle_order_schema.jsonify(order), 200


@orders_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 200
