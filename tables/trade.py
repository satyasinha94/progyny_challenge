from db_base.db_base import Base
from sqlalchemy import Column, String, Numeric, DateTime, Integer


class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True)
    coin_id = Column(String(20))
    quantity = Column(Numeric)
    price = Column(Numeric)
    trade_datetime = Column(DateTime)
