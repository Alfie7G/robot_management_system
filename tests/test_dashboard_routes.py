from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

#Dashboard integration and RBAC permission tests.

def unique_username() -> str:

    return f"testuser_{uuid4().hex[:8]}"


def test_dashboard_loads_successfully():

    client = TestClient(app)

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "Robot Management Dashboard" in response.text


def test_viewer_cannot_execute_dashboard_move(monkeypatch):

    username = unique_username()
    move_called = {"value": False}

    def fake_execute_robot_move(x, y, username="API"):
        move_called["value"] = True
        return {"success": True}

    monkeypatch.setattr(
        "app.api.dashboard_routes.execute_robot_move",
        fake_execute_robot_move
    )

    with TestClient(app) as client:
        client.post(
            "/register",
            data={"username": username, "password": "Password123"},
            follow_redirects=False
        )

        client.post(
            "/login",
            data={"username": username, "password": "Password123"},
            follow_redirects=False
        )

        response = client.post(
            "/dashboard/move",
            data={"x": 1, "y": 1},
            follow_redirects=False
        )

    assert response.status_code == 303
    assert move_called["value"] is False


def test_commander_can_execute_dashboard_move(monkeypatch):

    username = unique_username()
    move_called = {"value": False}

    def fake_execute_robot_move(x, y, username="API"):

        move_called["value"] = True
        return {"success": True}

    monkeypatch.setattr(
        "app.api.dashboard_routes.execute_robot_move",
        fake_execute_robot_move
    )

    with TestClient(app) as client:
        client.post(
            "/register",
            data={"username": username, "password": "Password123"},
            follow_redirects=False
        )

        client.post(f"/admin/promote/{username}")

        client.post(
            "/login",
            data={"username": username, "password": "Password123"},
            follow_redirects=False
        )

        response = client.post(
            "/dashboard/move",
            data={"x": 1, "y": 1},
            follow_redirects=False
        )

    assert response.status_code == 303
    assert move_called["value"] is True