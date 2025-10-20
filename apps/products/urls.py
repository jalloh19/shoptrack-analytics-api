from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product-list"),
    path("<uuid:id>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("create/", views.ProductCreateView.as_view(), name="product-create"),
    path("<uuid:id>/update/", views.ProductUpdateView.as_view(), name="product-update"),
    path("<uuid:id>/delete/", views.ProductDeleteView.as_view(), name="product-delete"),
]
