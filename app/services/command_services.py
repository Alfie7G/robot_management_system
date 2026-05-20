from app.database import session_local
from app.models.models import CommandLog
from app.services.robot_services import RobotAPIClient, RobotConnectionError

robot_client = RobotAPIClient()

# Execute a robot movement commad, and create an audit log entry.
def execute_robot_move(x: int, y: int, username: str = "API") -> dict: #Username defaults to api for unauthenticated api requests
    db = session_local()

    #Log the username, command type, and both the target x and y coordinates
    log = CommandLog(username=username, command_type="Move", target_x=x, target_y=y)


    #Try to move the robot to the given coordinates
    try:
        result = robot_client.move_robot(x,y)

        #If the move is valid, set the result of the move to success
        log.result = "Success"
        response = result

    #Validation failures here include invalid coordinates or an empty battery
    except ValueError as error:
        
        log.result = "Validation failed"
 
        response = {
            "success": False,
            "error": str(error)
        }
    
    #Incase the connection to the robot is lost
    except RobotConnectionError as error:

        #Logged separately from validation failures because they indicate API/infrastructure issues
        log.result ="Connection failed"

        #Also allows frontend to display the correct current connection
        response = {
            "connection": "offline",
            "error": str(error)
        }
    finally:
        try: 

            #Store a snapshot of the robots status along side the command
            status = robot_client.get_status()

            log.battery = str(status.get("battery"))
            log.robot_status = status.get("status")

        except RobotConnectionError:
            
            #If connection is lost after move but status is logged, still log the command attempt
            log.battery = None
            log.robot_status = "Unavailable"

        #Add the log to the database
        db.add(log)
        db.commit()
        db.close()
    
    return response
