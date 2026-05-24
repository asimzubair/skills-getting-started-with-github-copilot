"""
Shared fixtures for FastAPI tests.

This module provides fixtures that can be used across all test files.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src import app as app_module


# Store original activities for restoration between tests
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team for practice and matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim laps and improve technique in the school pool",
        "schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["nina@mergington.edu", "kevin@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["maya@mergington.edu", "liam@mergington.edu"]
    },
    "Drama Society": {
        "description": "Practice acting and put on school theater productions",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["sara@mergington.edu", "ethan@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Study challenging math problems and prepare for competitions",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
    },
    "Robotics Workshop": {
        "description": "Build robots and learn about engineering and automation",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["oliver@mergington.edu", "zara@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that resets the activities database before each test.
    
    This ensures that each test gets a fresh copy of the activities data,
    preventing test pollution (where one test's mutations affect another test).
    
    The autouse=True parameter means this fixture runs automatically for every test.
    """
    app_module.activities.clear()
    app_module.activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Cleanup after test
    app_module.activities.clear()
    app_module.activities.update(deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def client():
    """
    Fixture providing a FastAPI TestClient for making requests to the app.
    """
    return TestClient(app_module.app)


@pytest.fixture
def valid_email():
    """
    Fixture providing a valid test email that is not pre-registered.
    """
    return "test_student@mergington.edu"


@pytest.fixture
def activity_name():
    """
    Fixture providing a valid activity name that exists in the database.
    """
    return "Chess Club"


@pytest.fixture
def nonexistent_activity():
    """
    Fixture providing an activity name that doesn't exist.
    """
    return "Nonexistent Club"
