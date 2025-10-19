from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_name', 'product_price', 'quantity', 'added_at')
        read_only_fields = ('id', 'added_at')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'status', 'items', 'total_price', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())