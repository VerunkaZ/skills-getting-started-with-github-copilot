import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

original_activities = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(original_activities)
    yield


def test_root_redirects_to_static_index():
    # Arrange
    client = TestClient(app_module.app)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities():
    # Arrange
    client = TestClient(app_module.app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_for_activity_succeeds():
    # Arrange
    client = TestClient(app_module.app)
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_for_missing_activity_returns_404():
    # Arrange
    client = TestClient(app_module.app)
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Nonexistent/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400():
    # Arrange
    client = TestClient(app_module.app)
    email = "alex@mergington.edu"

    # Act
    response = client.post("/activities/Soccer%20Team/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_when_activity_is_full_returns_400():
    # Arrange
    client = TestClient(app_module.app)
    activity_name = "Art Studio"
    activity = app_module.activities[activity_name]
    activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]
    email = "latecomer@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name.replace(' ', '%20')}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
