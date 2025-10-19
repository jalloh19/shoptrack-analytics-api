import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.carts.models import Cart, CartItem
from apps.products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

try:
    # Get or create test user and product
    user, _ = User.objects.get_or_create(
        email='test@example.com',
        defaults={'username': 'testuser', 'password': 'testpass123'}
    )
    
    product, _ = Product.objects.get_or_create(
        name="Test Product for Cart",
        defaults={'price': 19.99, 'stock_quantity': 50, 'category': 'Test'}
    )
    
    # Test Cart creation
    cart = Cart.objects.create(user=user)
    print("✅ Cart created successfully!")
    print(f"Cart ID: {cart.id}")
    print(f"Cart User: {cart.user.email}")
    print(f"Cart Status: {cart.status}")
    
    # Test CartItem creation
    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)
    print("✅ CartItem created successfully!")
    print(f"CartItem: {cart_item}")
    print(f"Quantity: {cart_item.quantity}")
    print(f"Product: {cart_item.product.name}")
    
    # Test relationship
    print(f"✅ Cart has {cart.items.count()} items")
    
    # Clean up
    cart.delete()
    print("✅ Test data cleaned up!")
    
except Exception as e:
    print(f"❌ Error: {e}")