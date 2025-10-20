from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response

from .models import Product
from .serializers import (
    ProductCreateSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
)


class ProductListView(generics.ListAPIView):
    """
    List all products with search and filtering
    Public access - no authentication required
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category"]
    search_fields = ["name", "description"]


class ProductDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single product by ID
    Public access - no authentication required
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"


class ProductCreateView(generics.CreateAPIView):
    """
    Create a new product
    Admin access only
    """

    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.user.role != "admin" and not request.user.is_staff:
            self.permission_denied(
                request, message="Only admin users can create products"
            )


class ProductUpdateView(generics.UpdateAPIView):
    """
    Update an existing product
    Admin access only
    """

    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.user.role != "admin" and not request.user.is_staff:
            self.permission_denied(
                request, message="Only admin users can update products"
            )


class ProductDeleteView(generics.DestroyAPIView):
    """
    Delete a product
    Admin access only
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.user.role != "admin" and not request.user.is_staff:
            self.permission_denied(
                request, message="Only admin users can delete products"
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
