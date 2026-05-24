"""
Unit tests for activity management endpoints.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and fixtures
- Act: Call the function/endpoint being tested
- Assert: Verify the expected result or behavior
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


class TestGetActivities:
    """Tests for retrieving all activities."""
    
    def test_get_all_activities_returns_all_activities(self):
        """
        Arrange: Create a test client
        Act: Make a GET request to /activities
        Assert: Verify that all activities are returned with correct structure
        """
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities_data = response.json()
        assert isinstance(activities_data, dict)
        assert len(activities_data) == 9
        assert "Chess Club" in activities_data
        assert "Programming Class" in activities_data
    
    def test_get_activities_has_correct_structure(self):
        """
        Arrange: Create a test client
        Act: Make a GET request to /activities
        Assert: Verify each activity has the required fields
        """
        # Arrange
        client = TestClient(app)
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info, dict)
            assert set(activity_info.keys()) == required_fields
            assert isinstance(activity_info["participants"], list)
            assert isinstance(activity_info["max_participants"], int)


class TestSignupForActivity:
    """Tests for signing up a student to an activity."""
    
    def test_signup_with_valid_activity_and_email(self, activity_name, valid_email):
        """
        Arrange: Use fixtures for a valid activity name and email
        Act: POST to /activities/{activity_name}/signup with the email
        Assert: Verify signup is successful and returns correct message
        """
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": valid_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert valid_email in data["message"]
        assert activity_name in data["message"]
    
    def test_signup_to_nonexistent_activity_returns_404(self, valid_email, nonexistent_activity):
        """
        Arrange: Use a nonexistent activity name and valid email
        Act: POST to /activities/{nonexistent_activity}/signup
        Assert: Verify 404 error is returned with "Activity not found" message
        """
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": valid_email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_duplicate_signup_returns_400(self, activity_name, valid_email):
        """
        Arrange: Use a fresh email and sign up a student twice to the same activity
        Act: Try to sign up the same email twice
        Assert: Verify 400 error is returned with "already signed up" message on second attempt
        """
        # Arrange
        client = TestClient(app)
        
        # Act - First attempt (should succeed)
        response_first = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": valid_email}
        )
        
        # Act - Second attempt (should fail)
        response_second = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": valid_email}
        )
        
        # Assert
        assert response_first.status_code == 200
        assert response_second.status_code == 400
        data = response_second.json()
        assert data["detail"] == "Student already signed up for this activity"


class TestUnregisterFromActivity:
    """Tests for unregistering a student from an activity."""
    
    def test_unregister_existing_participant(self, activity_name):
        """
        Arrange: Use an activity and an email of an existing participant
        Act: DELETE from /activities/{activity_name}/unregister with that email
        Assert: Verify unregister is successful and returns correct message
        """
        # Arrange
        client = TestClient(app)
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert existing_email in data["message"]
        assert activity_name in data["message"]
    
    def test_unregister_from_nonexistent_activity_returns_404(self, valid_email, nonexistent_activity):
        """
        Arrange: Use a nonexistent activity name
        Act: DELETE from /activities/{nonexistent_activity}/unregister
        Assert: Verify 404 error is returned with "Activity not found" message
        """
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": valid_email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_unregister_nonexistent_participant_returns_404(self, activity_name, valid_email):
        """
        Arrange: Use a valid activity and an email not in the participants list
        Act: DELETE from /activities/{activity_name}/unregister with that email
        Assert: Verify 404 error is returned with "Participant not found" message
        """
        # Arrange
        client = TestClient(app)
        # Assuming valid_email is not in any activity initially
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": valid_email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Participant not found"
