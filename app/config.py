import os

Robot_API_URL = os.getenv("Robot_API_URL", "http://localhost:5000")
Robot_API_timeout = float(os.getenv("Robot_API_timeout", "3.0"))

SESSION_SECRET_KEY="robot_management_system_key_05_2026"