import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from tests.factories.user_factories import UserFactory, AdminUserFactory
from apps.products.models import Product
from apps.carts.models import Cart, CartItem
from apps.analytics.models import CartEvent

@pytest.mark.django_db
@pytest.mark.unit
class TestUserModel:
    def test_create_user(self):
        """Test creating a normal user"""
        user = UserFactory()
        assert user.email is not None
        assert user.role == 'customer'
        assert user.is_active is True
        assert user.is_staff is False
        
    def test_create_admin_user(self):
        """Test creating an admin user"""
        admin = AdminUserFactory()
        assert admin.role == 'admin'
        assert admin.is_staff is True
        
    def test_user_str_representation(self):
        """Test user string representation"""
        user = UserFactory(email='test@example.com')
        assert str(user) == 'test@example.com'

@pytest.mark.django_db
@pytest.mark.unit
class TestProductModel:
    def test_create_product(self):
        """Test creating a product"""
        product = Product(
            name="Test Product",
            description="Test Description",
            price=29.99,
            category="electronics",
            stock_quantity=100
        )
        product.save()
        
        assert product.name == "Test Product"
        assert product.price == 29.99
        assert product.stock_quantity == 100
        assert str(product) == "Test Product"

@pytest.mark.django_db
@pytest.mark.unit
class TestCartModel:
    def test_create_cart(self):
        """Test creating a cart for a user"""
        user = UserFactory()
        cart = Cart.objects.create(user=user, status='active')
        
        assert cart.user == user
        assert cart.status == 'active'
        assert cart.created_at is not None

@pytest.mark.django_db
@pytest.mark.unit
class TestCartItemModel:
    def test_create_cart_item(self):
        """Test adding item to cart"""
        user = UserFactory()
        cart = Cart.objects.create(user=user)
        product = Product.objects.create(
            name="Test Product",
            price=19.99,
            category="books",
            stock_quantity=50
        )
        
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=2
        )
        
        assert cart_item.cart == cart
        assert cart_item.product == product
        assert cart_item.quantity == 2