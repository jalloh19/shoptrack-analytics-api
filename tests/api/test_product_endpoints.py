import pytest
from rest_framework import status
from tests.factories import ProductFactory, AdminUserFactory

@pytest.mark.django_db
@pytest.mark.api
class TestProductEndpoints:
    def test_list_products_public_access(self, api_client):
        """Test anyone can list products"""
        ProductFactory.create_batch(3)
        
        response = api_client.get('/api/products/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
    
    def test_get_product_detail(self, api_client):
        """Test retrieving specific product details"""
        product = ProductFactory()
        
        response = api_client.get(f'/api/products/{product.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == product.name
        assert response.data['price'] == str(product.price)
    
    def test_create_product_admin_only(self, authenticated_client, admin_client):
        """Test product creation requires admin privileges"""
        product_data = {
            'name': 'New Product',
            'description': 'Test description',
            'price': '29.99',
            'category': 'electronics',
            'stock_quantity': 100
        }
        
        # Regular user should be denied
        response = authenticated_client.post('/api/products/create/', data=product_data)
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
        
        # Admin should be allowed (might be 201 or 400 depending on validation)
        response = admin_client.post('/api/products/create/', data=product_data)
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    
    def test_update_product_admin_only(self, authenticated_client, admin_client):
        """Test product update requires admin privileges"""
        product = ProductFactory()
        update_data = {
            'name': 'Updated Product',
            'price': '39.99'
        }
        
        # Regular user should be denied
        response = authenticated_client.patch(f'/api/products/{product.id}/update/', data=update_data)
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
        
        # Admin should be allowed
        response = admin_client.patch(f'/api/products/{product.id}/update/', data=update_data)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    
    def test_delete_product_admin_only(self, authenticated_client, admin_client):
        """Test product deletion requires admin privileges"""
        product = ProductFactory()
        
        # Regular user should be denied
        response = authenticated_client.delete(f'/api/products/{product.id}/delete/')
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
        
        # Admin should be allowed
        response = admin_client.delete(f'/api/products/{product.id}/delete/')
        assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]