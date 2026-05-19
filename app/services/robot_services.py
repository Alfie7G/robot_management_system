import httpx
from app.config import ROBOT_API_URL, ROBOT_API_TIMEOUT

class RobotConnectionError(Exception):
    pass

class RobotAPIClient:
   
    def __init__(self, base_url: str = ROBOT_API_URL):
        self.base_url = base_url.rstrip("/")
    
    def get_status(self) -> dict:
        return self._get("/api/status")
    
    def get_map(self) -> dict:
        return self._get("/api/map")
    
    def get_sensor_data(self) -> dict:
        return self._get("/api/sensor")
    
    def move_robot(self, x: int, y: int) -> dict:
        if not 0 <= x <= 20 or not 0 <= y <= 20:
            raise ValueError("Coordinates must remain between 0 and 20.")
        
        status = self.get_status()
        battery = status.get("battery", 0)

        if battery <=0:
            raise ValueError("Robot battery is empty")
        
        return self._post( "/api/move", json_data={"x": x, "y": y})
    
    def reset_simulation(self) -> dict:
        return self._post("/api/reset")
    

    ##
    def _get(self, endpoint: str) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}{endpoint}",
                timeout=ROBOT_API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()

        except httpx.TimeoutException as exc:
            raise RobotConnectionError("Robot API request timed out.") from exc

        except httpx.RequestError as exc:
            raise RobotConnectionError(f"Robot API unreachable: {exc}") from exc

        except httpx.HTTPStatusError as exc:
            raise RobotConnectionError(
                f"Robot API returned status {exc.response.status_code}: {exc.response.text}"
            ) from exc

    def _post(self, endpoint: str, json_data: dict | None = None) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}{endpoint}",
                json=json_data,
                timeout=ROBOT_API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()

        except httpx.TimeoutException as exc:
            raise RobotConnectionError("Robot API request timed out.") from exc

        except httpx.RequestError as exc:
            raise RobotConnectionError(f"Robot API unreachable: {exc}") from exc

        except httpx.HTTPStatusError as exc:
            raise RobotConnectionError(
                f"Robot API returned status {exc.response.status_code}: {exc.response.text}"
            ) from exc