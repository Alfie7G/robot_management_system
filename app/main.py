from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.services import RobotAPIClient, RobotConnectionError

app = FastAPI(title="Robot Management System")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
robot_client = RobotAPIClient()


@app.get("/")
def root():
    return {"message": "Robot Management System is running"}

# Robot API routes
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
    


# Dashboard and display routes
@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
    )

@app.get("/connection")
def dashboard_connection(request: Request):
    try:
        status = robot_client.get_status()
        connection = { "state": "online", "message": "Connected to the robot simulator"}

    except RobotConnectionError as error:
        connection = { "state": "offline", "message": str(error)}

    return templates.TemplateResponse(
        request=request,
        name="connection.html",
        context={
            "connection": connection
        }
    )


@app.get("/status")
def dashboard_status(request: Request):
    try:
        status = robot_client.get_status()
    except RobotConnectionError:
        status = None
    return templates.TemplateResponse(
        request=request,
        name="status.html",
        context={
            "status": status
        }
    )

@app.get("/map")
def dashboard_map(request: Request):
    try:
        status = robot_client.get_status()
        map = robot_client.get_map()
    except RobotConnectionError:
        status = None
        map = None
        
    return templates.TemplateResponse(
        request=request,
        name="map.html",
        context={
            "status": status,
            "map": map
        }
    )

@app.post("/dashboard/move")
def dashboard_move(x: int = Form(...), y: int = Form(...)):
    try: 
        robot_client.move_robot(x, y)
    except RobotConnectionError:
        pass
    except ValueError:
        pass
    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

@app.post("/dashboard/reset")
def dashboard_reset():
    try:
        robot_client.reset_simulation()
    except RobotConnectionError:
        pass
    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )    