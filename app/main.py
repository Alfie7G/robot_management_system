from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.api.robot_routes import robot_router
from app.api.dashboard_routes import dashboard_router
from app.api.auth_routes import auth_router

from app.models.models import CommandLog, User
from app.database import base, engine

from app.config import SESSION_SECRET_KEY

app = FastAPI(title="Robot Management System")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(SessionMiddleware, SESSION_SECRET_KEY)

#create tables on startup
base.metadata.create_all(bind=engine)

app.include_router(robot_router)
app.include_router(dashboard_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Robot Management System is running"}
