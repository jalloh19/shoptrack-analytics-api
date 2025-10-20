from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Cart, CartItem  # ADD CartItem import
from .serializers import CartItemCreateSerializer, CartItemSerializer, CartSerializer
from .services import CartService


class CartDetailView(generics.RetrieveAPIView):
    """Get current user's active cart with all items"""

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return CartService.get_or_create_user_cart(self.request.user)


class CartItemCreateView(generics.CreateAPIView):
    """Add item to user's cart using service layer"""

    serializer_class = CartItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart_item = CartService.add_item_to_cart(
                user=request.user,
                product=serializer.validated_data["product"],
                quantity=serializer.validated_data["quantity"],
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = CartItemSerializer(cart_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CartItemUpdateView(generics.UpdateAPIView):
    """Update cart item quantity using service layer"""

    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user, cart__status="active"
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            cart_item = CartService.update_cart_item_quantity(
                user=request.user,
                cart_item_id=instance.id,
                new_quantity=serializer.validated_data.get(
                    "quantity", instance.quantity
                ),
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = CartItemSerializer(cart_item)
        return Response(response_serializer.data)


class CartItemDeleteView(generics.DestroyAPIView):
    """Remove item from cart using service layer"""

    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user, cart__status="active"
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            CartService.remove_item_from_cart(request.user, instance.id)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Item removed from cart successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CartCheckoutView(generics.GenericAPIView):
    """Checkout cart and complete purchase"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def post(self, request):
        try:
            cart = CartService.checkout_cart(request.user)
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
