from db_base.db_base import Base
from sqlalchemy import Column, String, Numeric, Integer



class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    coin_id = Column(String(20))
    name = Column(String(20))
    symbol = Column(String(20))
    cost_basis = Column(Numeric)
    quantity = Column(Numeric(precision=2))
