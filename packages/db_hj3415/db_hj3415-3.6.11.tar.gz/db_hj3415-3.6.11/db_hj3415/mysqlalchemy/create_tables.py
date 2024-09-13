# create_tables.py - 이 코드는 한번만 실행되어 테이블을 생성하면 다음에는 실행할 필요 없다.
from db_hj3415.mysqlalchemy.database import engine, Base
from db_hj3415.mysqlalchemy.models import Stock, StockScore

# 테이블 생성
Base.metadata.create_all(engine)