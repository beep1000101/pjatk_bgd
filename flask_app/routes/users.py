from flask import Blueprint, request, jsonify
from sqlalchemy import select

from database.models.users import User
from flask_app.app import db
from flask_app.schemas.users import UserSchema
from flask_app.routes.errors import APIError
from flask_app.routes.utils.decorators import transactional

users_bp = Blueprint("users", __name__, url_prefix="/users")

single_user_schema = UserSchema()
multiple_users_schema = UserSchema(many=True)


@users_bp.post("")
@transactional("User already exists or violates a constraint.")
def create_user():
    data = request.get_json()
    errors = single_user_schema.validate(data)
    if errors:
        raise APIError(errors, 400)
    new_user = single_user_schema.load(data)
    db.session.add(new_user)
    db.session.flush()
    db.session.refresh(new_user)
    return jsonify(single_user_schema.dump(new_user)), 201


@users_bp.get("")
def get_users():
    users_selection_statement = select(User)
    users_list = db.session.execute(users_selection_statement).scalars().all()
    return jsonify(multiple_users_schema.dump(users_list)), 200


@users_bp.get("/<int:user_id>")
def get_user(user_id):
    user = db.session.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()
    if user is None:
        raise APIError("User not found", 404)
    return jsonify(single_user_schema.dump(user)), 200


@users_bp.put("/<int:user_id>")
@transactional("User update violates a constraint.")
def update_user(user_id):
    user = db.session.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()
    if user is None:
        raise APIError("User not found", 404)
    data = request.get_json()
    errors = single_user_schema.validate(data, partial=True)
    if errors:
        raise APIError(errors, 400)
    updated_user = single_user_schema.load(
        data, instance=user, partial=True
    )
    return jsonify(single_user_schema.dump(updated_user)), 200


@users_bp.delete("/<int:user_id>")
@transactional("User delete violates a constraint.")
def delete_user(user_id):
    user = db.session.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()
    if user is None:
        raise APIError("User not found", 404)
    db.session.delete(user)
    return jsonify({"message": "User deleted"}), 200
