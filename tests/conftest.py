import pytest
from django.conf import settings
from rest_framework.test import APIClient
from tests.factories import UserFactory, AdminUserFactory

@pytest.fixture
def api_client():
    """API client fixture for making requests"""
    return APIClient()

@pytest.fixture
def user():
    """Regular user fixture"""
    return UserFactory()

@pytest.fixture
def admin_user():
    """Admin user fixture"""
    return AdminUserFactory()

@pytest.fixture
def authenticated_client(user):
    """Authenticated API client with regular user"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def admin_client(admin_user):
    """Admin authenticated API client"""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client