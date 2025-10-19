from django.db import transaction
from .models import Cart, CartItem
from apps.analytics.models import CartEvent

class CartService:
    """Service class for cart business logic"""
    
    @staticmethod
    def get_or_create_user_cart(user):
        """Get or create active cart for user"""
        cart, created = Cart.objects.get_or_create(
            user=user,
            status='active'
        )
        return cart
    
    @staticmethod
    def add_item_to_cart(user, product, quantity):
        """Add item to cart with business logic"""
        with transaction.atomic():
            cart = CartService.get_or_create_user_cart(user)
            
            # Check stock availability
            if product.stock_quantity < quantity:
                raise ValueError(f"Only {product.stock_quantity} items available")
            
            # Update existing item or create new
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Update quantity if item exists
                new_quantity = cart_item.quantity + quantity
                if product.stock_quantity < new_quantity:
                    raise ValueError(f"Cannot add {quantity} more. Only {product.stock_quantity - cart_item.quantity} additional available")
                cart_item.quantity = new_quantity
                cart_item.save()
            
            # Log cart event
            CartEvent.objects.create(
                cart=cart,
                user=user,
                product=product,
                event_type='added',
                quantity_changed=quantity
            )
            
            return cart_item
    
    @staticmethod
    def update_cart_item_quantity(user, cart_item_id, new_quantity):
        """Update cart item quantity with validation"""
        with transaction.atomic():
            try:
                cart_item = CartItem.objects.select_related('product', 'cart').get(
                    id=cart_item_id,
                    cart__user=user,
                    cart__status='active'
                )
            except CartItem.DoesNotExist:
                raise ValueError("Cart item not found")
            
            if new_quantity < 1:
                raise ValueError("Quantity must be at least 1")
            
            if cart_item.product.stock_quantity < new_quantity:
                raise ValueError(f"Only {cart_item.product.stock_quantity} items available")
            
            # Calculate quantity change for analytics
            quantity_change = new_quantity - cart_item.quantity
            
            cart_item.quantity = new_quantity
            cart_item.save()
            
            # Log cart event
            if quantity_change != 0:
                CartEvent.objects.create(
                    cart=cart_item.cart,
                    user=user,
                    product=cart_item.product,
                    event_type='updated',
                    quantity_changed=quantity_change
                )
            
            return cart_item
    
    @staticmethod
    def remove_item_from_cart(user, cart_item_id):
        """Remove item from cart"""
        with transaction.atomic():
            try:
                cart_item = CartItem.objects.select_related('product', 'cart').get(
                    id=cart_item_id,
                    cart__user=user,
                    cart__status='active'
                )
            except CartItem.DoesNotExist:
                raise ValueError("Cart item not found")
            
            # Log cart event before deletion
            CartEvent.objects.create(
                cart=cart_item.cart,
                user=user,
                product=cart_item.product,
                event_type='removed',
                quantity_changed=-cart_item.quantity
            )
            
            cart_item.delete()
    
    @staticmethod
    def calculate_cart_totals(cart):
        """Calculate cart totals and item count"""
        items = cart.items.select_related('product').all()
        
        total_price = sum(item.product.price * item.quantity for item in items)
        items_count = sum(item.quantity for item in items)
        
        return {
            'total_price': total_price,
            'items_count': items_count,
            'unique_items': len(items)
        }
    
    @staticmethod
    def checkout_cart(user):
        """Simulate cart checkout"""
        with transaction.atomic():
            cart = CartService.get_or_create_user_cart(user)
            
            if cart.items.count() == 0:
                raise ValueError("Cannot checkout empty cart")
            
            # Validate stock for all items
            for item in cart.items.select_related('product').all():
                if item.product.stock_quantity < item.quantity:
                    raise ValueError(f"Not enough stock for {item.product.name}")
            
            # Update cart status
            cart.status = 'purchased'
            cart.save()
            
            # Log purchase event
            CartEvent.objects.create(
                cart=cart,
                user=user,
                event_type='purchased'
            )
            
            return cart