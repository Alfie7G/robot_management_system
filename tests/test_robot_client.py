import pytest

from app.services.services import RobotAPIClient


def test_move_robot_rejects_negative_x_coordinate():
    client = RobotAPIClient()

    with pytest.raises(ValueError):
        client.move_robot(-1, 5)


def test_move_robot_rejects_negative_y_coordinate():
    client = RobotAPIClient()

    with pytest.raises(ValueError):
        client.move_robot(5, -1)


def test_move_robot_rejects_x_coordinate_above_grid_limit():
    client = RobotAPIClient()

    with pytest.raises(ValueError):
        client.move_robot(21, 5)


def test_move_robot_rejects_y_coordinate_above_grid_limit():
    client = RobotAPIClient()

    with pytest.raises(ValueError):
        client.move_robot(5, 21)