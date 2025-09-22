import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from app.models import Project

@pytest.mark.django_db
def test_unauthenticated_user_cannot_list_projects():
    client = APIClient()
    response = client.get('/api/v1/projects/')
    assert response.status_code == 401

@pytest.mark.django_db
def test_user_can_only_see_their_own_projects():
    client = APIClient()
    user_a = User.objects.create_user(username='user_a', password='password123')
    user_b = User.objects.create_user(username='user_b', password='password123')

    project_a_title = 'Projeto do usuario A'
    project_a = Project.objects.create(title=project_a_title)
    project_a.members.add(user_a)

    project_b = Project.objects.create(title='Projeto do usuario B')
    project_b.members.add(user_b)

    client.force_authenticate(user=user_a)

    response = client.get('/api/v1/projects/')
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]['title'] == project_a_title