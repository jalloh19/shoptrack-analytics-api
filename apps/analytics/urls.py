from django.urls import path

from . import views

app_name = "analytics"

urlpatterns = [
    path(
        "abandonment-rate/",
        views.AbandonmentRateView.as_view(),
        name="abandonment-rate",
    ),
    path(
        "user-behavior/<uuid:user_id>/",
        views.UserBehaviorView.as_view(),
        name="user-behavior",
    ),
    path(
        "product-insights/<uuid:product_id>/",
        views.ProductInsightsView.as_view(),
        name="product-insights",
    ),
    path("time-metrics/", views.TimeMetricsView.as_view(), name="time-metrics"),
    path("daily-metrics/", views.DailyMetricsView.as_view(), name="daily-metrics"),
    path(
        "frequently-added-together/",
        views.FrequentlyAddedTogetherView.as_view(),
        name="frequently-added-together",
    ),
]
