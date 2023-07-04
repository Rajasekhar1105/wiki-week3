from sqlalchemy import column,Integer,String

from database import Base

class Articles(Base):
    __tablename__ = "articles"
    id = column(Integer,primary_key=True,index=True)
    title = column(String)
    content=column(String)
    