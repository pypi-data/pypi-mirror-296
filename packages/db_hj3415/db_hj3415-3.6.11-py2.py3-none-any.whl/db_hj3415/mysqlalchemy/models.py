# models.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from db_hj3415.mysqlalchemy.database import Base

# Stock 모델
class Corp(Base):
    __tablename__ = 'corps'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    daily_scores = relationship("DailyScores", back_populates="Corp")

    def __repr__(self):
        return f"<Corp(code={self.code}, name={self.name})>"

# StockPrice 모델
class DailyScores(Base):
    __tablename__ = 'daily_scores'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    red = Column(Integer, nullable=True)


    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

    stock_id = Column(Integer, ForeignKey('stocks.id'), nullable=False)
    stock = relationship("Stock", back_populates="scores")

    def __repr__(self):
        return (f"<StockPrice(date={self.date}, open_price={self.open_price}, "
                f"close_price={self.close_price}, high_price={self.high_price}, "
                f"low_price={self.low_price}, volume={self.volume})>")