import httpx
from app.config import ROBOT_API_URL, ROBOT_API_TIMEOUT

#When the dashboard cannot communicate with the robot API
class RobotConnectionError(Exception):
    pass

#Client wrapper for the virtual robot REST API
class RobotAPIClient:
   
    def __init__(self, base_url: str = ROBOT_API_URL):
        self.base_url = base_url.rstrip("/")
    
    #Retrieve current robot status, e.g. battery.
    def get_status(self) -> dict:
        return self._get("/api/status")
    
    #Retrieve current 2d map from the simulator
    def get_map(self) -> dict:
        return self._get("/api/map")
    
    #Retrieve proximity sensor data from the simulator
    def get_sensor_data(self) -> dict:
        return self._get("/api/sensor")
    
    #Validate and send the robot a movement command
    def move_robot(self, x: int, y: int) -> dict:

        #Ensures coordinates are equal to or between 0 and 20
        if not 0 <= x <= 20 or not 0 <= y <= 20:
            raise ValueError("Coordinates must remain between 0 and 20.")
        

        status = self.get_status()
        battery = status.get("battery", 0)

        #Ensures battery is not empty
        if battery <=0:
            raise ValueError("Robot battery is empty")
        
        return self._post( "/api/move", json_data={"x": x, "y": y})
    
    #Reset the simulation state
    def reset_simulation(self) -> dict:
        return self._post("/api/reset")
    

    #Send a GET request to the robot API, and handle connection errors.
    def _get(self, endpoint: str) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}{endpoint}",
                timeout=ROBOT_API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()

        #All timeout, network and http errors are converted into RobotConnectionError, so the UI can handle API failures consistently.
        except httpx.TimeoutException as exc:
            raise RobotConnectionError("Robot API request timed out.") from exc

        except httpx.RequestError as exc:
            raise RobotConnectionError(f"Robot API unreachable: {exc}") from exc

        except httpx.HTTPStatusError as exc:
            raise RobotConnectionError(
                f"Robot API returned status {exc.response.status_code}: {exc.response.text}"
            ) from exc

    #Send a POST request to the robot API, and again handle connection errors
    def _post(self, endpoint: str, json_data: dict | None = None) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}{endpoint}",
                json=json_data,
                timeout=ROBOT_API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()

        #Again, all timeout, network and http errors are converted into RobotConnectionError
        except httpx.TimeoutException as exc:
            raise RobotConnectionError("Robot API request timed out.") from exc

        except httpx.RequestError as exc:
            raise RobotConnectionError(f"Robot API unreachable: {exc}") from exc

        except httpx.HTTPStatusError as exc:
            raise RobotConnectionError(
                f"Robot API returned status {exc.response.status_code}: {exc.response.text}"
            ) from exc