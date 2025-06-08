from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from flask_app.app import db
from database.models.users import User


class UserSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow schema for serializing and deserializing User objects.
    """

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field(required=True)
    email = auto_field(required=True)
    city = auto_field()
