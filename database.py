from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database configuration
# URL_DATABASE = 'mysql+pymysql://root:password@localhost:3306/flask'
URL_DATABASE = 'mysql+pymysql://admin:password@database-1.cx64aigk03po.us-east-1.rds.amazonaws.com/flask'

engine = create_engine(URL_DATABASE)

sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()