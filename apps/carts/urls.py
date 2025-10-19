from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart-detail'),
    path('items/', views.CartItemCreateView.as_view(), name='cartitem-create'),
    path('items/<uuid:id>/', views.CartItemUpdateView.as_view(), name='cartitem-update'),
    path('items/<uuid:id>/delete/', views.CartItemDeleteView.as_view(), name='cartitem-delete'),
]
