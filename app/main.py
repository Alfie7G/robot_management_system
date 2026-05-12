from fastapi import FastAPI

from app.services.services import RobotAPIClient, RobotConnectionError


app = FastAPI(title="Robot Management System")

robot_client = RobotAPIClient()


@app.get("/")
def root():
    return {"message": "Robot Management System is running"}


@app.get("/robot/status")
def get_robot_status():
    try: 
        return robot_client.get_status()
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }
    
@app.get("/robot/map")
def get_robot_map():
    try: 
        return robot_client.get_map()
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }

@app.get("/robot/sensor")
def get_robot_sensor_data():
    try: 
        return robot_client.get_sensor_data()
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }

@app.post("/robot/move/{x}/{y}")
def move_robot_to(x: int, y: int):
    try: 
        return robot_client.move_robot(x, y)
    except ValueError as error:
        return {
            "success": False,
            "error": str(error)
        }
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }

@app.post("/robot/reset")
def reset_simulation():
    try: 
        return robot_client.reset_simulation()
    except RobotConnectionError as error:
        return {
            "connection": "offline",
            "error": str(error)
        }