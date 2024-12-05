from ..constants import *

import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()
username = os.getenv('POSTGRES_USERNAME', DEFAULT_POSTGRES_USER)
password = os.getenv('POSTGRES_PASSWORD', DEFAULT_POSTGRES_PASSWORD)
database_url = os.getenv('POSTGRES_URL', DEFAULT_POSTGRES_URL)
connection_db_url = f"postgresql://{username}:{password}@{database_url}"

engine = create_engine(connection_db_url)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_new_scoped_session():
    return scoped_session(db_session)

# We have one db_session per thread.  Note that if we can have multiple transactions
# running at the same time in a thread (i.e., overlapping in time), then we would
# need to create more sessions; we cannot rely on a single db_session in that case.
db_session = get_new_scoped_session()

Base = declarative_base()
Base.query = db_session.query_property()