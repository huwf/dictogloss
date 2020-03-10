from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from server.constants import DB_CONNECTION_STRING

engine = create_engine(DB_CONNECTION_STRING, connect_args={'check_same_thread': False})

db = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)



