from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.database import session_local
from app.models.models import User




client = TestClient(app)

def unique_username() -> str:

    return f"testuser_{uuid4().hex[:8]}"


def test_register_creates_user():

    username = unique_username()

    response = client.post(
        "/register",
        data={
            "username": username,
            "password": "Password123"
        },
        follow_redirects=False
    )

    assert response.status_code == 303

    db = session_local()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    assert user is not None
    assert user.username == username
    assert user.role == "Viewer"
    assert user.password_hash != "Password123"


def test_register_does_not_create_non_unique_user():

    username = unique_username()

    client.post(
        "/register",
        data={
            "username": username,
            "password": "Password123"
        },
        follow_redirects=False
    )

    response = client.post(
        "/register",
        data={
            "username": username,
            "password": "DifferentPassword123"
        },
        follow_redirects=False
    )

    assert response.status_code == 303

    db = session_local()
    users = db.query(User).filter(User.username == username).all()
    db.close()

    assert len(users) == 1

def test_login():

    username = unique_username()

    with TestClient(app) as session_client:
        session_client.post(
            "/register",
            data={
                "username": username,
                "password": "Password123"
            },
            follow_redirects=False
        )

        session_client.post(
            "/login",
            data={
                "username": username,
                "password": "Password123"
            },
            follow_redirects=False
        )

        response = session_client.get("/dashboard")

        assert username in response.text


def test_logout():
    
    username = unique_username()

    with TestClient(app) as session_client:
        session_client.post(
            "/register",
            data={
                "username": username,
                "password": "Password123"
            },
            follow_redirects=False
        )

        session_client.post(
            "/login",
            data={
                "username": username,
                "password": "Password123"
            },
            follow_redirects=False
        )

        session_client.post(
            "/logout",
            follow_redirects=False
        )

        response = session_client.get("/dashboard")

        assert username not in response.text