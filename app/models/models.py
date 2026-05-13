from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC

from app.database import base

class CommandLog(base):

    __tablename__ = "command_logs",

    id = Column(Integer, primary_key = True, index = True)

    command_type = Column(String, nullable = False)

    target_x = Column(Integer, nullable = False)
    target_y = Column(Integer, nullable = False)

    result = Column(String, nullable = False)

    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))