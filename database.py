from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./articles.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args ={'cheeck_same_thread':False})

sessionLocal = sessionmaker(autocomit=False,autoflush=False,bind=engine)

Base = declarative_base()