from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from app.auth.security import hash_password, verify_password
from app.database import session_local
from app.models.models import User

auth_router = APIRouter()

@auth_router.post("/register")
def register(username: str, password: str):

    db = session_local()

    existing_user = (db.query(User).filter(User.username == username).first())

    if existing_user:
        db.close()

        return{
            "success" : False,
            "error" : "That username already exsists"
        }
    
    new_user = User(username = username, password_hash = hash_password(password))

    db.add(new_user)
    db.commit()
    db.close()

    return{
        "success" : True,
        "error" : "User registered"
    }

@auth_router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = session_local()

    user = (db.query(User).filter(User.username == username).first())

    if not user or not verify_password(password, user.password_hash):
        db.close()
        return{
            "success" : False,
            "error" : "Invalid username or password"
        }

    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["role"] = user.role

    db.close()

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

@auth_router.post("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

