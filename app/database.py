from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#SQLite database file for local persistence
DATABASE_URL = "sqlite:///./app/data/robot_management.db"

#SQAlchemy engine manages the connection to the SQLite database
engine = create_engine( DATABASE_URL, connect_args={"check_same_thread": False})

#Creates database sessions used by routes/services
session_local = sessionmaker(autocommit = False, autoflush = False, bind=engine)

#Base class that all SQAlchemy models inherit from
base = declarative_base()