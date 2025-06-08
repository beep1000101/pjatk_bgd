from flask import Blueprint, request, jsonify

from database.models.users import User
from flask_app.app import db
from flask_app.schemas.users import UserSchema

users_bp = Blueprint("users", __name__, url_prefix="/users")

single_user_schema = UserSchema()
multiple_users_schema = UserSchema(many=True)


@users_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json()
    errors = single_user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return single_user_schema.jsonify(user), 201


@users_bp.route("", methods=["GET"])
def get_users():
    users = User.query.all()
    return multiple_users_schema.jsonify(users), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return single_user_schema.jsonify(user), 200


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    errors = single_user_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return single_user_schema.jsonify(user), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
