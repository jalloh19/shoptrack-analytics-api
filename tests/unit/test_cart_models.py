import pytest
from tests.factories import CartFactory, CartItemFactory, UserFactory, ProductFactory

@pytest.mark.django_db
@pytest.mark.unit
class TestCartModel:
    def test_cart_creation(self):
        """Test basic cart creation"""
        cart = CartFactory()
        assert cart.user is not None
        assert cart.status == 'active'
        assert cart.created_at is not None
        
    def test_cart_status_choices(self):
        """Test cart status choices"""
        cart = CartFactory()
        valid_statuses = ['active', 'abandoned', 'purchased']
        assert cart.status in valid_statuses
        
    def test_cart_string_representation(self):
        """Test cart string representation"""
        user = UserFactory(email='test@example.com')
        cart = CartFactory(user=user)
        assert str(cart) == f"Cart {cart.id} - test@example.com"

@pytest.mark.django_db
@pytest.mark.unit
class TestCartItemModel:
    def test_cart_item_creation(self):
        """Test cart item creation"""
        cart_item = CartItemFactory()
        assert cart_item.cart is not None
        assert cart_item.product is not None
        assert cart_item.quantity >= 1
        
    def test_cart_item_unique_together(self):
        """Test cart item unique constraint"""
        cart = CartFactory()
        product = ProductFactory()
        
        # First item should work
        CartItemFactory(cart=cart, product=product, quantity=1)
        
        # Second item with same cart and product should raise IntegrityError
        with pytest.raises(Exception):  # Could be IntegrityError or ValidationError
            CartItemFactory(cart=cart, product=product, quantity=2)
            
    def test_cart_item_string_representation(self):
        """Test cart item string representation"""
        product = ProductFactory(name="Test Product")
        cart_item = CartItemFactory(product=product, quantity=3)
        assert str(cart_item) == "3 x Test Product"