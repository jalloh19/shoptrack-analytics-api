import pytest
from decimal import Decimal
from tests.factories import ProductFactory

@pytest.mark.django_db
@pytest.mark.unit
class TestProductModel:
    def test_product_creation(self):
        """Test basic product creation"""
        product = ProductFactory()
        assert product.name is not None
        assert isinstance(product.price, Decimal)
        assert product.stock_quantity >= 0
        
    def test_product_string_representation(self):
        """Test product string representation"""
        product = ProductFactory(name="Test Product")
        assert str(product) == "Test Product"
        
    def test_product_fields(self):
        """Test all product fields exist"""
        product = ProductFactory.build()
        assert hasattr(product, 'name')
        assert hasattr(product, 'description')
        assert hasattr(product, 'price')
        assert hasattr(product, 'category')
        assert hasattr(product, 'stock_quantity')