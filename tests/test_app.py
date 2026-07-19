from fastapi.testclient import TestClient

from src import app as app_module


def test_duplicate_signup_is_rejected():
    client = TestClient(app_module.app)

    response = client.post(
        "/activities/Chess%20Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 200

    response = client.post(
        "/activities/Chess%20Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregistering_participant_removes_them_from_activity():
    client = TestClient(app_module.app)
    original_participants = list(app_module.activities["Chess Club"]["participants"])

    try:
        response = client.post(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
        assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
    finally:
        app_module.activities["Chess Club"]["participants"] = original_participants
