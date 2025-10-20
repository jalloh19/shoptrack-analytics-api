import pytest
from rest_framework import status
from tests.factories import ProductFactory

@pytest.mark.django_db
@pytest.mark.integration
class TestErrorScenarios:
    def test_out_of_stock_scenario(self, authenticated_client):
        """Test handling out of stock items"""
        product = ProductFactory(stock_quantity=2)  # Low stock
        
        # Try to add more than available
        cart_data = {
            'product': product.id,
            'quantity': 5  # More than available stock
        }
        response = authenticated_client.post('/api/carts/items/', data=cart_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'stock' in str(response.data).lower() or 'available' in str(response.data).lower()
    
    def test_unauthorized_access_scenarios(self, api_client, authenticated_client):
        """Test unauthorized access attempts"""
        # Try to access profile without authentication
        profile_response = api_client.get('/api/auth/profile/')
        assert profile_response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Try to create product as regular user
        product_data = {
            'name': 'Unauthorized Product',
            'price': '29.99',
            'stock_quantity': 10
        }
        create_response = authenticated_client.post('/api/products/create/', data=product_data)
        assert create_response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
    
    def test_invalid_data_scenarios(self, authenticated_client):
        """Test handling of invalid data"""
        # Invalid product ID
        invalid_cart_data = {
            'product': 'invalid-uuid-format',
            'quantity': 1
        }
        response = authenticated_client.post('/api/carts/items/', data=invalid_cart_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Negative quantity
        product = ProductFactory()
        negative_quantity_data = {
            'product': product.id,
            'quantity': -1
        }
        response = authenticated_client.post('/api/carts/items/', data=negative_quantity_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST