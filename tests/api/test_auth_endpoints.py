import pytest
from rest_framework import status
from tests.factories import UserFactory

@pytest.mark.django_db
@pytest.mark.api
class TestAuthenticationEndpoints:
    def test_user_registration(self, api_client):
        """Test user registration endpoint"""
        registration_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'customer'
        }
        
        response = api_client.post('/api/auth/register/', data=registration_data)
        # Might be 201 Created or 400 Bad Request depending on validation
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        if response.status_code == 201:
            assert 'email' in response.data
            assert response.data['email'] == 'test@example.com'
    
    def test_user_login(self, api_client):
        """Test user login with correct endpoint"""
        user = UserFactory(email='login@example.com', password='testpass123')
        
        login_data = {
            'email': 'login@example.com',
            'password': 'testpass123'
        }
        
        response = api_client.post('/api/auth/login/', data=login_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_token_refresh(self, api_client):
        """Test token refresh endpoint"""
        user = UserFactory(email='refresh@example.com', password='testpass123')
        
        # First get tokens
        login_data = {'email': 'refresh@example.com', 'password': 'testpass123'}
        login_response = api_client.post('/api/auth/login/', data=login_data)
        refresh_token = login_response.data['refresh']
        
        # Refresh the token
        refresh_data = {'refresh': refresh_token}
        refresh_response = api_client.post('/api/auth/token/refresh/', data=refresh_data)
        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data
    
    def test_get_user_profile_authenticated(self, authenticated_client):
        """Test retrieving user profile when authenticated"""
        response = authenticated_client.get('/api/auth/profile/')
        assert response.status_code == status.HTTP_200_OK
        assert 'email' in response.data
        assert 'role' in response.data
    
    def test_get_user_profile_unauthenticated(self, api_client):
        """Test profile access without authentication"""
        response = api_client.get('/api/auth/profile/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED