from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.robot_services import RobotAPIClient, RobotConnectionError
from app.services.command_services import execute_robot_move
from app.database import session_local
from app.models.models import CommandLog

dashboard_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

robot_client = RobotAPIClient()

@dashboard_router.get("/dashboard")
def dashboard(request: Request):
    auth_error = request.session.pop("auth_error", None)
    auth_success = request.session.pop("auth_success", None)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"current_user": request.session, "auth_error": auth_error, "auth_success": auth_success}
    )

@dashboard_router.get("/connection")
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


@dashboard_router.get("/status")
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

@dashboard_router.get("/map")
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

@dashboard_router.post("/dashboard/move")
def dashboard_move(request: Request, x: int = Form(...), y: int = Form(...)):
    
    if request.session.get("role") != "Commander":
        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )
    
    execute_robot_move(x,y, username=request.session.get("username"))

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

@dashboard_router.post("/dashboard/reset")
def dashboard_reset(request: Request):
        
    if request.session.get("role") != "Commander":
        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )
    

    robot_client.reset_simulation()

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )    
