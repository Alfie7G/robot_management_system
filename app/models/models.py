from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC

from app.database import base

#Audit log table used to persistently store robot command activity along
#with the relevent status data for saftey tracking
class CommandLog(base):

    __tablename__ = "command_logs"

    id = Column(Integer, primary_key = True, index = True)

    command_type = Column(String, nullable = False)

    username = Column(String, nullable = False)

    target_x = Column(Integer, nullable = False)
    target_y = Column(Integer, nullable = False)

    result = Column(String, nullable = False)

    battery = Column(String, nullable=True)

    robot_status = Column(String, nullable=True)

    #UTC timestamps to avoid timezone inconsistency
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))

#Datanase model representing registered users
class User(base):

    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)

    username = Column(String, unique = True, nullable = False)

    #Passwords are stored as hashes, not plaintext
    password_hash = Column(String, nullable = False)

    #New accounts default to viewer role.
    role = Column(String, default = "Viewer")