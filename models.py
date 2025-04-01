from sqlalchemy import Column,Integer,String
from sqlalchemy.dialects.mysql import LONGTEXT
from database import Base

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer,index=True,unique=True)
    title = Column(String(100))
    author = Column(String(50))
    content = Column(LONGTEXT)
    meta_data = Column(LONGTEXT)