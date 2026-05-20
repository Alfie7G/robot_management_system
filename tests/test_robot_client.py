import pytest

from app.services.robot_services import RobotAPIClient

#Validation tests for robot movement safety rules and contraints

def test_move_robot_rejects_negative_x_coordinate():

    client = RobotAPIClient()

    with pytest.raises(ValueError):
        client.move_robot(-1, 5)


def test_move_robot_rejects_negative_y_coordinate():

    client = RobotAPIClient()

    with pytest.raises(ValueError):
        client.move_robot(5, -1)


def test_move_robot_rejects_x_above_grid_limit():

    client = RobotAPIClient()

    with pytest.raises(ValueError):
        client.move_robot(21, 5)


def test_move_robot_rejects_y_above_grid_limit():

    client = RobotAPIClient()

    with pytest.raises(ValueError):
        client.move_robot(5, 21)


def test_move_robot_rejects_empty_battery(monkeypatch):
    
    client = RobotAPIClient()

    #Mock robot telemetry so the test doesnt depend on live sim
    def fake_status():
        return {"battery": 0}

    monkeypatch.setattr(client, "get_status", fake_status)

    with pytest.raises(ValueError):
        client.move_robot(1, 1)