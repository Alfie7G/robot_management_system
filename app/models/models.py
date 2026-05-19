from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC

from app.database import base

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

    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))


class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)

    username = Column(String, unique = True, nullable = False)

    password_hash = Column(String, nullable = False)

    role = Column(String, default = "Viewer")