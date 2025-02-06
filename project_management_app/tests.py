import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from project_management_app.models import Project, Task

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin_user", password="adminpass", role="admin")

@pytest.fixture
def member_user(db):
    return User.objects.create_user(username="member_user", password="memberpass", role="member")

@pytest.fixture
def project(admin_user):
    return Project.objects.create(title="Test Project", description="Test Description", creator=admin_user)

@pytest.fixture
def task(project):
    return Task.objects.create(title="Test Task", description="Test Task Description", project=project, status="to_do")


@pytest.mark.django_db
def test_admin_can_create_project(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        "/api/projects/",  
        {"title": "Django Project 1", "description": "Test Description"},  
        format="json"
    )

    print("Response Data:", response.data)  # Debugging
    assert response.status_code == 201
    assert response.data["title"] == "Django Project 1"
    assert response.data["creator"] == admin_user.username  # Validate creator

@pytest.mark.django_db
def test_member_cannot_create_project(api_client, member_user):
    """Ensure a non-admin member cannot create a project"""
    api_client.force_authenticate(user=member_user)

    response = api_client.post(
        "/api/projects/",
        {"title": "Unauthorized Project", "description": "Should not be allowed"},
        format="json"
    )

    assert response.status_code == 403  # Forbidden


@pytest.mark.django_db
def test_member_can_create_task(api_client, member_user, project):
    """Ensure a member can create a task under an existing project"""
    api_client.force_authenticate(user=member_user)

    response = api_client.post(
        "/api/tasks/",
        {"title": "New Task", "description": "Task Description", "project": project.id},
        format="json"
    )

    assert response.status_code == 201
    assert response.data["title"] == "New Task"
    assert response.data["project"] == project.id


@pytest.mark.django_db
def test_member_can_update_task_status(api_client, member_user, task):
    """Ensure a member can update a task's status"""
    api_client.force_authenticate(user=member_user)

    response = api_client.patch(f"/api/tasks/{task.id}/update_status/", {"status": "in_progress"}, format="json")

    assert response.status_code == 200
    assert response.data["status"] == "updated"


@pytest.mark.django_db
def test_admin_cannot_update_task_status(api_client, admin_user, task):
    """Ensure an admin cannot update a task's status"""
    api_client.force_authenticate(user=admin_user)

    response = api_client.patch(f"/api/tasks/{task.id}/update_status/", {"status": "completed"}, format="json")

    assert response.status_code == 403  # Forbidden
