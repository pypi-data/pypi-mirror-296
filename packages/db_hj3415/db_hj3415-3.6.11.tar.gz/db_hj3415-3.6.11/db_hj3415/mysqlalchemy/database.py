# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 데이터베이스 연결
engine = create_engine('sqlite:///stocks.db', echo=True)

# 세션 설정
Session = sessionmaker(bind=engine)

# 베이스 클래스 설정
Base = declarative_base()

def get_session():
    """세션을 생성하고 반환하는 함수"""
    return Session()