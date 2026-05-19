import os

ROBOT_API_URL = os.getenv("ROBOT_API_URL", "http://localhost:5000")
ROBOT_API_TIMEOUT = float(os.getenv("Robot_API_timeout", "3.0"))

SESSION_SECRET_KEY="robot_management_system_key_05_2026"