import pytest
from django.conf import settings
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """API client fixture for making requests"""
    return APIClient()

@pytest.fixture
def authenticated_client(user):
    """Authenticated API client"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def admin_client(admin_user):
    """Admin authenticated API client"""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client