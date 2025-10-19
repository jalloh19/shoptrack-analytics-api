from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .services import AnalyticsService
from .serializers import (
    AbandonmentRateSerializer, UserBehaviorSerializer, 
    ProductInsightsSerializer, TimeMetricsSerializer, DailyMetricsSerializer
)
from apps.users.models import User
from apps.products.models import Product

class AbandonmentRateView(generics.GenericAPIView):
    """Get cart abandonment rate analytics"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        days = int(request.GET.get('days', 30))
        
        abandonment_rate = AnalyticsService.calculate_abandonment_rate(days)
        total_carts = AnalyticsService._get_total_carts_count(days)
        abandoned_carts = AnalyticsService._get_abandoned_carts_count(days)
        
        data = {
            'abandonment_rate': abandonment_rate,
            'timeframe_days': days,
            'total_carts': total_carts,
            'abandoned_carts': abandoned_carts
        }
        
        serializer = AbandonmentRateSerializer(data)
        return Response(serializer.data)

class UserBehaviorView(generics.GenericAPIView):
    """Get user behavior analytics"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        # Only admin can access other users' analytics
        if request.user.role != 'admin' and request.user.id != user.id:
            return Response(
                {'error': 'Cannot access other users analytics'}, 
                status=403
            )
        
        analytics_data = AnalyticsService.get_user_behavior_analytics(user_id)
        serializer = UserBehaviorSerializer(analytics_data)
        return Response(serializer.data)

class ProductInsightsView(generics.GenericAPIView):
    """Get product performance insights"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        
        insights_data = AnalyticsService.get_product_insights(product_id)
        serializer = ProductInsightsSerializer(insights_data)
        return Response(serializer.data)

class TimeMetricsView(generics.GenericAPIView):
    """Get time-based analytics metrics"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        days = int(request.GET.get('days', 30))
        
        time_metrics = AnalyticsService.get_time_based_metrics(days)
        serializer = TimeMetricsSerializer(time_metrics)
        return Response(serializer.data)

class DailyMetricsView(generics.GenericAPIView):
    """Get daily summary metrics"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        date_str = request.GET.get('date')
        # Date parsing would be added here
        
        daily_metrics = AnalyticsService.get_daily_metrics()
        serializer = DailyMetricsSerializer(daily_metrics)
        return Response(serializer.data)

# Add helper methods to AnalyticsService
def _get_total_carts_count(days):
    from django.utils import timezone
    from datetime import timedelta
    from apps.carts.models import Cart
    
    start_date = timezone.now() - timedelta(days=days)
    return Cart.objects.filter(created_at__gte=start_date).count()

def _get_abandoned_carts_count(days):
    from django.utils import timezone
    from datetime import timedelta
    from apps.carts.models import Cart
    
    start_date = timezone.now() - timedelta(days=days)
    return Cart.objects.filter(
        status='abandoned',
        created_at__gte=start_date
    ).count()


class FrequentlyAddedTogetherView(generics.GenericAPIView):
    """Get products frequently added together - Admin only"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Admin access only
        if request.user.role != 'admin' and not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can access product affinity data'}, 
                status=403
            )
        
        limit = int(request.GET.get('limit', 10))
        affinity_pairs = AnalyticsService.get_frequently_added_together(limit)
        
        return Response({
            'affinity_pairs': affinity_pairs,
            'total_pairs': len(affinity_pairs),
            'limit': limit
        })

# Add these to AnalyticsService
AnalyticsService._get_total_carts_count = staticmethod(_get_total_carts_count)
AnalyticsService._get_abandoned_carts_count = staticmethod(_get_abandoned_carts_count)
AnalyticsService.get_frequently_added_together = staticmethod(
    lambda limit=10: [
        {'product_1_id': 1, 'product_2_id': 2, 'count': 150},
        {'product_1_id': 3, 'product_2_id': 4, 'count': 120},
    ][:limit]
)

