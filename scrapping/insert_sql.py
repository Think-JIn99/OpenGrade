from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import datetime

Base = declarative_base()

def get_score():
    """
    성적 데이터를 토대로 점수를 계산한다.
    """


class User(Base):
    """
    ORM활용을 위한 테이블 객체를 정의합니다. 
    """
    __tablename__ = "user" #사용할 테이블 이름

    studentId = Column(Integer, primary_key=True)
    phl = Column(Integer)
    math = Column(Integer)
    bigData = Column(Integer)
    programming = Column(Integer)
    businessManagement= Column(Integer)
    department = Column(String)
    com_score = Column(Float)
    soft_score = Column(Float)
    updateDate = Column(DateTime)


    def __init__(self, student_id, phl, math, big_data, programming, business_management, department, com_score, soft_score, update_date):
        self.studentId = student_id
        self.phl = phl
        self.math = math
        self.bigData = big_data
        self.programming = programming
        self.businessManagement = business_management
        self.department = department
        self.com_score = com_score
        self.soft_score = soft_score
        self.updateDate = update_date


def insert_data_db(insert_data:dict):
    """
    DB 유저 테이블에 데이터를 삽입합니다.

    Args:
        student_id (int): 학번
        phl (int): 성적
        math (int): 성적
        big_data (int): 성적
        programming (int): 성적
        business_management (int): 성적
        department (int): 성적
        score (int): 총합점수
        update_date (datetime): 최신 업데이트 일수

    Returns:
        _type_: _description_
    """
    #gcp 유저와 비밀번호
    engine = create_engine(f"mysql+pymysql://root:<my_pass>@34.64.94.74:3306/grade", encoding='utf-8')
    user = User(**insert_data)
    session = Session(engine) #세션을 생성
    session.add(user) #세션에 SQL을 추가
    try:
        session.commit() #SQL 디비에 전송
        session.close()
        return True #DB 삽입이 문제 없이 종료

    except TimeoutError as e: #DB 연결을 위한 시간이 너무 오래 걸리는 경우
        print("Exception in insert data to DB", e)

    except IntegrityError as e: #기본 키 등의 제약이 지켜지지 않은 경우
        print("Integirity Violence Errror!", e)



if __name__ == "__main__":
    
    now = datetime.datetime.now() #현재시각
    
    #더미 데이터 입니다.
    insert_data = {'student_id':20191305, 'phl':97, 'math':95, 'big_data':93, 'programming':90, 'business_management':88, 
    'department':"컴", 'com_score':0, 'soft_score':0, 'update_date':now}
    user = insert_data_db(insert_data)
    