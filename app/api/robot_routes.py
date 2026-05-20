from fastapi import APIRouter

from app.services.robot_services import RobotAPIClient, RobotConnectionError
from app.services.command_services import execute_robot_move

robot_router = APIRouter()

robot_client = RobotAPIClient()

#Return live robot telemetry directly from simulator api
@robot_router.get("/robot/status")
def get_robot_status():

    try:
        return robot_client.get_status()
    
    #Incase of connection error, return offline response instead of crashing the API route
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }

#Return the current map state
@robot_router.get("/robot/map")
def get_robot_map():

    try:
        return robot_client.get_map()
    
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }

#Return live robot sensor data
@robot_router.get("/robot/sensor")
def get_robot_sensor_data():

    try:
        return robot_client.get_sensor_data()
    
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }

#Execute a robot movement command through the shared service layer
@robot_router.post("/robot/move/{x}/{y}")
def move_robot_to(x: int, y: int):

    return execute_robot_move(x, y)

#Reset the robot simulation
@robot_router.post("/robot/reset")
def reset_simulation():

    try:
        return robot_client.reset_simulation()
    
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }
