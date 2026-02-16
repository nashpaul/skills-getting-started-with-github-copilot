from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity keys exist
    assert "Basketball" in data


def test_signup_and_unregister_flow():
    activity = "Basketball"
    email = "test.student@example.com"

    # Ensure email not already present
    resp = client.get("/activities")
    assert resp.status_code == 200
    before = resp.json()[activity]["participants"].copy()
    if email in before:
        # remove if already present to start clean
        client.delete(f"/activities/{activity}/signup?email={email}")

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json().get("message")

    # Verify participant present
    resp = client.get("/activities")
    parts = resp.json()[activity]["participants"]
    assert email in parts

    # Unregister
    resp = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json().get("message")

    # Verify participant removed
    resp = client.get("/activities")
    parts_after = resp.json()[activity]["participants"]
    assert email not in parts_after
