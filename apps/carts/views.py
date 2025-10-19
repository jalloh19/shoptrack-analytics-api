from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartItemCreateSerializer

class CartDetailView(generics.RetrieveAPIView):
    """
    Get current user's active cart with all items
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user,
            status='active'
        )
        return cart

class CartItemCreateView(generics.CreateAPIView):
    """
    Add item to user's cart
    """
    serializer_class = CartItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Get or create user's active cart
        cart, created = Cart.objects.get_or_create(
            user=self.request.user,
            status='active'
        )
        
        # Check if item already exists in cart
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        
        existing_item = CartItem.objects.filter(cart=cart, product=product).first()
        
        if existing_item:
            # Update quantity if item exists
            new_quantity = existing_item.quantity + quantity
            if product.stock_quantity < new_quantity:
                raise ValidationError({
                    'quantity': f'Cannot add {quantity} more. Only {product.stock_quantity - existing_item.quantity} additional items available'
                })
            existing_item.quantity = new_quantity
            existing_item.save()
            self.instance = existing_item
        else:
            # Create new cart item
            serializer.save(cart=cart)

class CartItemUpdateView(generics.UpdateAPIView):
    """
    Update cart item quantity
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # Users can only update items in their own cart
        return CartItem.objects.filter(cart__user=self.request.user, cart__status='active')

    def perform_update(self, serializer):
        instance = self.get_object()
        new_quantity = serializer.validated_data.get('quantity', instance.quantity)
        
        if new_quantity < 1:
            raise ValidationError({"quantity": "Quantity must be at least 1"})
        
        if instance.product.stock_quantity < new_quantity:
            raise ValidationError({
                "quantity": f"Only {instance.product.stock_quantity} items available in stock"
            })
        
        serializer.save()

class CartItemDeleteView(generics.DestroyAPIView):
    """
    Remove item from cart
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # Users can only delete items from their own cart
        return CartItem.objects.filter(cart__user=self.request.user, cart__status='active')
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Item removed from cart successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )
