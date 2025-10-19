from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartDetailView(generics.RetrieveAPIView):
    """
    Get current user's active cart
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
    Add item to cart
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class CartItemUpdateView(generics.UpdateAPIView):
    """
    Update cart item quantity
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class CartItemDeleteView(generics.DestroyAPIView):
    """
    Remove item from cart
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
