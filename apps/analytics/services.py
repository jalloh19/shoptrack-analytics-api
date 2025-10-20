from datetime import timedelta
from django.utils import timezone
from apps.carts.models import Cart
from apps.products.models import Product
from .models import CartEvent
from django.db.models import Count


class AnalyticsService:
    """Service class for analytics calculations"""

    @staticmethod
    def calculate_abandonment_rate(days=30):
        """Calculate cart abandonment rate for given period"""
        start_date = timezone.now() - timedelta(days=days)

        total_carts = Cart.objects.filter(created_at__gte=start_date).count()
        abandoned_carts = Cart.objects.filter(
            status="abandoned", created_at__gte=start_date
        ).count()

        if total_carts == 0:
            return 0

        abandonment_rate = (abandoned_carts / total_carts) * 100
        return round(abandonment_rate, 2)

    @staticmethod
    def get_user_behavior_analytics(user_id):
        """Get comprehensive analytics for a specific user"""
        user_carts = Cart.objects.filter(user_id=user_id)
        user_events = CartEvent.objects.filter(user_id=user_id)

        # Basic metrics
        total_carts = user_carts.count()
        purchased_carts = user_carts.filter(status="purchased").count()
        abandoned_carts = user_carts.filter(status="abandoned").count()

        # Cart value analysis
        cart_values = []
        for cart in user_carts.filter(status="purchased"):
            total = sum(item.product.price * item.quantity for item in cart.items.all())
            cart_values.append(float(total))

        avg_cart_value = sum(cart_values) / len(cart_values) if cart_values else 0

        # Product affinity
        product_interactions = (
            user_events.filter(event_type__in=["added", "purchased"])
            .values("product__name")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        return {
            "user_id": user_id,
            "total_carts": total_carts,
            "purchase_rate": (
                round((purchased_carts / total_carts * 100), 2) if total_carts else 0
            ),
            "abandonment_rate": (
                round((abandoned_carts / total_carts * 100), 2) if total_carts else 0
            ),
            "average_cart_value": round(avg_cart_value, 2),
            "favorite_products": list(product_interactions),
            "total_interactions": user_events.count(),
        }

    @staticmethod
    def get_product_insights(product_id):
        """Get analytics for a specific product"""
        product_events = CartEvent.objects.filter(product_id=product_id)

        # Event counts by type
        event_counts = product_events.values("event_type").annotate(count=Count("id"))

        # Conversion rate (added to purchased)
        added_count = product_events.filter(event_type="added").count()
        purchased_count = product_events.filter(event_type="purchased").count()

        conversion_rate = (purchased_count / added_count * 100) if added_count else 0

        # Time-based analysis (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_events = product_events.filter(timestamp__gte=thirty_days_ago)

        return {
            "product_id": product_id,
            "total_interactions": product_events.count(),
            "event_breakdown": list(event_counts),
            "conversion_rate": round(conversion_rate, 2),
            "recent_activity": recent_events.count(),
            "abandonment_count": product_events.filter(event_type="abandoned").count(),
        }

    @staticmethod
    def get_time_based_metrics(days=30):
        """Get time-based analytics metrics"""
        start_date = timezone.now() - timedelta(days=days)

        recent_events = CartEvent.objects.filter(timestamp__gte=start_date)
        recent_carts = Cart.objects.filter(created_at__gte=start_date)

        # Session duration analysis (simplified)
        cart_sessions = []
        for cart in recent_carts:
            events = CartEvent.objects.filter(cart=cart).order_by("timestamp")
            if events.count() > 1:
                duration = (
                    events.last().timestamp - events.first().timestamp
                ).total_seconds()
                cart_sessions.append(duration)

        avg_session_duration = (
            sum(cart_sessions) / len(cart_sessions) if cart_sessions else 0
        )

        # Event frequency
        events_by_day = (
            recent_events.extra({"date": "DATE(timestamp)"})
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        return {
            "timeframe_days": days,
            "total_carts": recent_carts.count(),
            "total_events": recent_events.count(),
            "average_session_duration_seconds": round(avg_session_duration, 2),
            "daily_activity": list(events_by_day),
            "most_active_hour": AnalyticsService._get_most_active_hour(recent_events),
        }

    @staticmethod
    def get_frequently_added_together(limit=10):
        """Find products frequently added to cart together"""
        from django.db import connection

        # This is a simplified implementation
        # In production, you might use more advanced querying

        cart_items_query = """
        SELECT ci1.product_id as product1, ci2.product_id as product2, COUNT(*) as 
        frequency
        FROM cart_items ci1
        JOIN cart_items ci2 ON ci1.cart_id = ci2.cart_id AND 
        ci1.product_id < ci2.product_id
        GROUP BY ci1.product_id, ci2.product_id
        ORDER BY frequency DESC
        LIMIT %s
        """

        with connection.cursor() as cursor:
            cursor.execute(cart_items_query, [limit])
            results = cursor.fetchall()

        affinity_pairs = []
        for product1_id, product2_id, frequency in results:
            try:
                product1 = Product.objects.get(id=product1_id)
                product2 = Product.objects.get(id=product2_id)
                affinity_pairs.append(
                    {
                        "product_a": {"id": product1.id, "name": product1.name},
                        "product_b": {"id": product2.id, "name": product2.name},
                        "frequency": frequency,
                    }
                )
            except Product.DoesNotExist:
                continue

        return affinity_pairs

    @staticmethod
    def _get_most_active_hour(events_queryset):
        """Helper method to find most active hour"""
        from django.db.models.functions import ExtractHour

        hour_activity = (
            events_queryset.annotate(hour=ExtractHour("timestamp"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("-count")
            .first()
        )

        return hour_activity["hour"] if hour_activity else None

    @staticmethod
    def get_daily_metrics(date=None):
        """Get daily summary metrics"""
        if date is None:
            date = timezone.now().date()

        day_start = timezone.make_aware(
            timezone.datetime.combine(date, timezone.datetime.min.time())
        )
        day_end = day_start + timedelta(days=1)

        daily_events = CartEvent.objects.filter(timestamp__range=[day_start, day_end])
        daily_carts = Cart.objects.filter(created_at__range=[day_start, day_end])

        return {
            "date": date.isoformat(),
            "active_carts": daily_carts.filter(status="active").count(),
            "completed_purchases": daily_carts.filter(status="purchased").count(),
            "abandoned_carts": daily_carts.filter(status="abandoned").count(),
            "total_events": daily_events.count(),
            "new_users": 0,  # Would need user registration dates
        }
