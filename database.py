from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedAsDataclass
# from sqlalchemy.ext.declarative import declarative_base
import pymysql



# Create a connection to the database
URL_DATABASE = "mysql+pymysql://avnadmin:AVNS_lLZKkrB87wusYgDKJpP@mysql-5ffef73-ojopeter36-c17c.g.aivencloud.com:12886/bincom"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase, MappedAsDataclass):
    pass