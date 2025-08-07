import datetime
import os
import tempfile
from unittest.mock import patch, MagicMock

from database import MallDatabase, NotificationLog
from app.services import push_service


def _mock_response(success=True):
    mock = MagicMock()
    mock.status_code = 200 if success else 500
    mock.json.return_value = {"success": 1 if success else 0}
    mock.content = b"{}"
    return mock


def _fresh_db():
    fd, path = tempfile.mkstemp(prefix="mq_test", suffix=".db")
    os.close(fd)
    return MallDatabase(f"sqlite:///{path}")


def test_send_push_logs_success():
    db = _fresh_db()
    db.add_user({"user_id": "u1", "name": "Test", "email": "t@example.com"})
    with patch("app.services.push_service.requests.post", return_value=_mock_response()):
        assert push_service.send_push("u1", "hello", db_instance=db)
    session = db._session_for_key("u1")
    logs = session.query(NotificationLog).filter_by(user_id="u1").all()
    assert len(logs) == 1 and logs[0].delivered is True
    session.close()


def test_send_retention_push_targets_dormant_users():
    db = _fresh_db()
    old = datetime.datetime.utcnow() - datetime.timedelta(days=31)
    db.add_user({"user_id": "u1", "name": "Dormant", "email": "d@example.com", "updated_at": old})
    db.add_user({"user_id": "u2", "name": "Active", "email": "a@example.com"})
    with patch("app.services.push_service.requests.post", return_value=_mock_response()):
        sent = push_service.send_retention_push(db_instance=db, days=30)
    assert sent == 1
    session = db._session_for_key("u1")
    assert session.query(NotificationLog).filter_by(user_id="u1").count() == 1
    session.close()


def test_send_push_retries_on_failure():
    db = _fresh_db()
    db.add_user({"user_id": "u1", "name": "Test", "email": "t@example.com"})
    with patch("app.services.push_service.requests.post", side_effect=Exception) as post:
        assert push_service.send_push("u1", "hi", retries=2, db_instance=db) is False
        assert post.call_count == 2
    session = db._session_for_key("u1")
    log = session.query(NotificationLog).first()
    assert log.delivered is False
    session.close()
