from rest_framework import serializers

from .models import CartEvent


class CartEventSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = CartEvent
        fields = (
            "id",
            "event_type",
            "user_email",
            "product_name",
            "quantity_changed",
            "timestamp",
            "session_duration_seconds",
        )


class AbandonmentRateSerializer(serializers.Serializer):
    abandonment_rate = serializers.FloatField()
    timeframe_days = serializers.IntegerField()
    total_carts = serializers.IntegerField()
    abandoned_carts = serializers.IntegerField()


class UserBehaviorSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    total_carts = serializers.IntegerField()
    purchase_rate = serializers.FloatField()
    abandonment_rate = serializers.FloatField()
    average_cart_value = serializers.FloatField()
    favorite_products = serializers.ListField()
    total_interactions = serializers.IntegerField()


class ProductInsightsSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    total_interactions = serializers.IntegerField()
    event_breakdown = serializers.ListField()
    conversion_rate = serializers.FloatField()
    recent_activity = serializers.IntegerField()
    abandonment_count = serializers.IntegerField()


class TimeMetricsSerializer(serializers.Serializer):
    timeframe_days = serializers.IntegerField()
    total_carts = serializers.IntegerField()
    total_events = serializers.IntegerField()
    average_session_duration_seconds = serializers.FloatField()
    daily_activity = serializers.ListField()
    most_active_hour = serializers.IntegerField(allow_null=True)


class DailyMetricsSerializer(serializers.Serializer):
    date = serializers.CharField()
    active_carts = serializers.IntegerField()
    completed_purchases = serializers.IntegerField()
    abandoned_carts = serializers.IntegerField()
    total_events = serializers.IntegerField()
    new_users = serializers.IntegerField()
