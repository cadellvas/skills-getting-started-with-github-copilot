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
