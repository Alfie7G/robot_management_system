from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.api.robot_routes import robot_router
from app.api.dashboard_routes import dashboard_router
from app.api.auth_routes import auth_router

from app.database import base, engine

from app.config import SESSION_SECRET_KEY

app = FastAPI(title="Robot Management System")

#Serve CSS frontend asset
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#Session middleware enables persistent login/authentication sessions
app.add_middleware(SessionMiddleware, SESSION_SECRET_KEY)

#Create database tables automatically on startup
base.metadata.create_all(bind=engine)

#Register application routes
app.include_router(robot_router)
app.include_router(dashboard_router)
app.include_router(auth_router)

#On startup redirect users to the main dashboard interface
@app.get("/")
def root():

    return RedirectResponse(url="/dashboard")
