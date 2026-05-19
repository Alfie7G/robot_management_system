from app.database import session_local
from app.models.models import CommandLog
from app.services.robot_services import RobotAPIClient, RobotConnectionError

robot_client = RobotAPIClient()

def execute_robot_move(x: int, y: int, username: str = "API") -> dict: #username defaults to api for unauthenticated api requests
    db = session_local()

    log = CommandLog(username=username, command_type="Move", target_x=x, target_y=y)

    try:
        result = robot_client.move_robot(x,y)

        
        log.result = "Success"
        response = result

    except ValueError as error:
        
        log.result = "Failed"
 
        response = {
            "success": False,
            "error": str(error)
        }
    except RobotConnectionError as error:

        log.result ="Failed"

        response = {
            "connection": "offline",
            "error": str(error)
        }
    finally:
        try: 

            status = robot_client.get_status()

            log.battery = str(status.get("battery"))
            log.robot_status = status.get("status")

        except RobotConnectionError:
            
            log.battery = None
            log.robot_status = "Unavailable"

        
        db.add(log)
        db.commit()
        db.close()
    
    return response
