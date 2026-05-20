from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from app.auth.security import hash_password, verify_password
from app.database import session_local
from app.models.models import User

auth_router = APIRouter()

#Register a new user account with a hashed password
@auth_router.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...)):

    db = session_local()

    existing_user = (db.query(User).filter(User.username == username).first())

    #Check that the user doesnt already exsist, ie if the username already exsists within the database
    if existing_user:
        db.close()

        #Display to UI
        request.session["auth_error"] = "That username already exists."
        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )
    
    #Passwords are hashed before storage so plaintext credentials are never saved
    new_user = User(username = username, password_hash = hash_password(password))

    #Add the new user details to the database
    db.add(new_user)
    db.commit()
    db.close()

    #Display to UI
    request.session["auth_success"] = "Account created. Please log in."
    return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

#Authenticate a user and store their role in the session
@auth_router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = session_local()

    user = (db.query(User).filter(User.username == username).first())

    #Verify name and or password is correct
    if not user or not verify_password(password, user.password_hash):
        db.close()

        #Output inavalid username OR password, not both, does not give out any more info than necessary
        request.session["auth_error"] = "Invalid username or password"
        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    #Session data is used by dashboard routes to identify a users role to enforce RBAC
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["role"] = user.role

    db.close()

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

#Clear the active user session
@auth_router.post("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

#Promote a user to Commander
@auth_router.post("/admin/promote/{username}")
def promote_user(username: str):
    db = session_local()

    user = (db.query(User).filter(User.username == username).first())

    #Incase the user does not exsist
    if not user:
        db.close()
        return {
            "success": False,
            "error": "User not found"
        }
    
    #Commander users can send movement/reset commands
    user.role = "Commander"

    db.commit()
    db.close()

    return {
        "success": True,
        "message": f"{username} promoted to Commander"
    }

#Demote a user to a viewer
@auth_router.post("/admin/demote/{username}")
def demote_user(username: str):
    db = session_local()

    user = (db.query(User).filter(User.username == username).first())

    #Incase the user does not exsist
    if not user:
        db.close()
        return {
            "success": False,
            "error": "User not found"
        }
    
    #Viewer users can only view, they cannot interact with the robot simulation
    user.role = "Viewer"

    db.commit()
    db.close()

    return {
        "success": True,
        "message": f"{username} demoted to Viewer"
    }