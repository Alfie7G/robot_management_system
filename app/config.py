import os

Robot_API_URL = os.getenv("Robot_API_URL", "http://localhost:5000")
Robot_API_timeout = float(os.getenv("Robot_API_timeout", "3.0"))

