from app.database import session_local
from app.models.models import CommandLog
from app.services.command_services import execute_robot_move


def test_execute_robot_move_creates_command_log(monkeypatch):
    def fake_move_robot(x, y):
        return {"success": True}

    def fake_get_status():
        return {
            "battery": 95.0,
            "status": "IDLE"
        }

    monkeypatch.setattr(
        "app.services.command_services.robot_client.move_robot",
        fake_move_robot
    )

    monkeypatch.setattr(
        "app.services.command_services.robot_client.get_status",
        fake_get_status
    )

    response = execute_robot_move(3, 4, username="test_user")

    db = session_local()
    log = (
        db.query(CommandLog)
        .filter(CommandLog.username == "test_user")
        .order_by(CommandLog.id.desc())
        .first()
    )
    db.close()

    assert response == {"success": True}
    assert log is not None
    assert log.username == "test_user"
    assert log.command_type == "Move"
    assert log.target_x == 3
    assert log.target_y == 4
    assert log.result == "Success"
    assert log.battery == "95.0"
    assert log.robot_status == "IDLE"