from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from flask_app.app import db
from database.models.orders import Order


class OrderSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow schema for serializing and deserializing Order objects.
    """

    class Meta:
        model = Order
        sqla_session = db.session
        load_instance = True
        include_fk = True

    id = auto_field(dump_only=True)
    customer_id = auto_field(required=True)
    product = auto_field(required=True)
    quantity = auto_field()
    total_price = auto_field()
    order_date = auto_field()
