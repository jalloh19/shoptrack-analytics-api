import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.products.models import Product

# Test creating a product
try:
    product = Product.objects.create(
        name="Test Product",
        description="A test product for validation",
        price=29.99,
        category="Electronics",
        stock_quantity=100
    )
    print("✅ Product created successfully!")
    print(f"Product ID: {product.id}")
    print(f"Product Name: {product.name}")
    print(f"Product Price: ${product.price}")
    print(f"Stock Quantity: {product.stock_quantity}")
    
    # Test retrieval
    retrieved_product = Product.objects.get(id=product.id)
    print("✅ Product retrieval successful!")
    
    # Test string representation
    print(f"✅ String representation: {retrieved_product}")
    
    # Clean up
    product.delete()
    print("✅ Test product cleaned up!")
    
except Exception as e:
    print(f"❌ Error: {e}")