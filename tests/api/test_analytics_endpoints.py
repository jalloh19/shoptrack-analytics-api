import pytest
from rest_framework import status
from tests.factories import UserFactory, ProductFactory, CartEventFactory


@pytest.mark.django_db
@pytest.mark.api
class TestAnalyticsEndpoints:
    def test_abandonment_rate_admin_access(self, admin_client, authenticated_client):
        """Test abandonment rate endpoint requires admin access"""
        # Regular user should be denied
        response = authenticated_client.get('/api/analytics/abandonment-rate/')
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
        
        # Admin should be allowed
        response = admin_client.get('/api/analytics/abandonment-rate/')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    
    def test_user_behavior_analytics(self, admin_client, authenticated_client):
        """Test user behavior analytics endpoint"""
        user = UserFactory()
        
        # Regular user should be denied access to other users' data
        response = authenticated_client.get(f'/api/analytics/user-behavior/{user.id}/')
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
        
        # Admin should be allowed
        response = admin_client.get(f'/api/analytics/user-behavior/{user.id}/')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    def test_product_insights_admin_access(self, admin_client, authenticated_client):
        """Test product insights endpoint requires admin access"""
        product = ProductFactory()
        
        # Regular user should be denied
        response = authenticated_client.get(f'/api/analytics/product-insights/{product.id}/')
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
        
        # Admin should be allowed
        response = admin_client.get(f'/api/analytics/product-insights/{product.id}/')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    
    def test_time_metrics_admin_access(self, admin_client, authenticated_client):
        """Test time metrics endpoint requires admin access"""
        # Regular user should be denied
        response = authenticated_client.get('/api/analytics/time-metrics/')
        allowed_statuses = [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
        assert response.status_code in allowed_statuses
        
        # Admin should be allowed
        response = admin_client.get('/api/analytics/time-metrics/')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    
    def test_daily_metrics_admin_access(self, admin_client, authenticated_client):
        """Test daily metrics endpoint requires admin access"""
        # Regular user should be denied
        response = authenticated_client.get('/api/analytics/daily-metrics/')
        allowed_statuses = [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

        assert response.status_code in allowed_statuses
        
        # Admin should be allowed
        response = admin_client.get('/api/analytics/daily-metrics/')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    
    def test_frequently_added_together_admin_access(
        self,
        admin_client,
        authenticated_client,
    ):

        """Test frequently added together endpoint requires admin access"""
        # Regular user should be denied
        response = authenticated_client.get('/api/analytics/frequently-added-together/')
        allowed_statuses = [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
        assert response.status_code in allowed_statuses
        
        # Admin should be allowed
        response = admin_client.get('/api/analytics/frequently-added-together/')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]