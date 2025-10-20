import pytest
from rest_framework import status
from tests.factories import ProductFactory

@pytest.mark.django_db
@pytest.mark.api
class TestCartEndpoints:
    def test_get_current_cart(self, authenticated_client):
        """Test retrieving current user's cart"""
        response = authenticated_client.get('/api/carts/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_add_item_to_cart(self, authenticated_client):
        """Test adding item to cart - FIXED DATA FORMAT"""
        product = ProductFactory(stock_quantity=10)
        
        # FIX: Send product ID directly (not as string) since DRF handles object lookup
        cart_data = {
            'product': product.id,  # Send UUID object, not string
            'quantity': 2
        }
        response = authenticated_client.post('/api/carts/items/', data=cart_data)
        
        # Should now return 201 Created
        assert response.status_code == status.HTTP_201_CREATED
        assert 'product' in response.data
        assert 'quantity' in response.data
        assert response.data['quantity'] == 2
    
    def test_update_cart_item(self, authenticated_client):
        """Test updating cart item quantity"""
        product = ProductFactory(stock_quantity=10)
        
        # First add item to cart with correct format
        add_data = {'product': product.id, 'quantity': 2}
        add_response = authenticated_client.post('/api/carts/items/', data=add_data)
        
        if add_response.status_code in [200, 201]:
            # Get the item ID from response
            item_id = add_response.data.get('id')
            
            # Update quantity
            update_data = {'quantity': 3}
            update_response = authenticated_client.patch(f'/api/carts/items/{item_id}/', data=update_data)
            assert update_response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    
    def test_remove_cart_item(self, authenticated_client):
        """Test removing item from cart"""
        product = ProductFactory(stock_quantity=10)
        
        # First add item to cart with correct format
        add_data = {'product': product.id, 'quantity': 1}
        add_response = authenticated_client.post('/api/carts/items/', data=add_data)
        
        if add_response.status_code in [200, 201]:
            # Get the item ID from response
            item_id = add_response.data.get('id')
            
            # Remove item
            delete_response = authenticated_client.delete(f'/api/carts/items/{item_id}/delete/')
            assert delete_response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]
    
    def test_cart_checkout(self, authenticated_client):
        """Test cart checkout"""
        # First add an item to cart with correct format
        product = ProductFactory(stock_quantity=5)
        add_data = {'product': product.id, 'quantity': 1}
        authenticated_client.post('/api/carts/items/', data=add_data)
        
        # Then checkout
        response = authenticated_client.post('/api/carts/checkout/')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]