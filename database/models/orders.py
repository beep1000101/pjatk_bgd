from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date

from database.models.base import Base


class Order(Base):
    """
    Represents an order in the database.
    """
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    total_price = Column(Float)
    order_date = Column(Date)
