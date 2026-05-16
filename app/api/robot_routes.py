from fastapi import APIRouter

from app.services.robot_services import RobotAPIClient, RobotConnectionError
from app.services.command_services import execute_robot_move

robot_router = APIRouter()

robot_client = RobotAPIClient()

@robot_router.get("/robot/status")
def get_robot_status():
    try:
        return robot_client.get_status()
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }

@robot_router.get("/robot/map")
def get_robot_map():
    try:
        return robot_client.get_map()
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }

@robot_router.get("/robot/sensor")
def get_robot_sensor_data():
    try:
        return robot_client.get_sensor_data()
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }

@robot_router.post("/robot/move/{x}/{y}")
def move_robot_to(x: int, y: int):
    return execute_robot_move(x, y)

@robot_router.post("/robot/reset")
def reset_simulation():
    try:
        return robot_client.reset_simulation()
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }