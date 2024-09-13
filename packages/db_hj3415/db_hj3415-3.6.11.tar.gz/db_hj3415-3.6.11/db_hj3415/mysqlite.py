# main.py
from db_hj3415.mysqlalchemy.models import Stock, StockScore
from db_hj3415.mysqlalchemy.database import get_session
from datetime import date

# 데이터 삽입
def add_stock():
    session = get_session()

    samsung = Stock(code="005930", name="Samsung Electronics")
    session.add(samsung)
    session.commit()

    samsung_price = StockPrice(
        stock=samsung,
        date=date(2024, 9, 12),
        open_price=70000.00,
        close_price=71000.00,
        high_price=72000.00,
        low_price=69000.00,
        volume=1500000
    )
    session.add(samsung_price)
    session.commit()

    session.close()

# 데이터 조회
def get_stocks():
    session = get_session()

    stocks = session.query(Stock).all()
    for stock in stocks:
        print(stock)

    session.close()

# 데이터 삭제
def delete_stock(stock_code):
    session = get_session()

    stock = session.query(Stock).filter_by(code=stock_code).first()
    if stock:
        session.delete(stock)
        session.commit()

    session.close()

# 실행
if __name__ == '__main__':
    add_stock()
    get_stocks()
    delete_stock("005930")