import os

#Base URL for the robot simulator API
ROBOT_API_URL = os.getenv("ROBOT_API_URL", "http://localhost:5000")

#Maximum wait time for robot API requests before timing out
ROBOT_API_TIMEOUT = float(os.getenv("ROBOT_API_TIMEOUT", "3.0"))

#Secret key used to sign and protect session data
SESSION_SECRET_KEY="robot_management_system_key_CMP9134"