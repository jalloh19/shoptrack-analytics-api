from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Import your custom admin site - REMOVE the default admin imports
from apps.core.admin import admin_site

# Enhanced Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="🛍️ ShopTrack Analytics API",
        default_version="v1.0.0",
        description=(
            "## 🚀 Complete E-commerce Analytics Solution\n\n"
            "Track shopping cart behavior, analyze abandonment rates, "
            "and gain data-driven insights to boost your e-commerce performance.\n\n"
            
            "### 📊 Core Features\n"
            "- **Real-time Cart Analytics** - Monitor active shopping sessions\n"
            "- **User Behavior Tracking** - Understand customer journey patterns\n"
            "- **Abandonment Rate Analysis** - Identify and reduce cart abandonment\n"
            "- **Product Performance Insights** - Optimize your product catalog\n"
            "- **Behavioral Analytics** - Data-driven decision making\n\n"
            
            "### 🔐 Authentication\n"
            "Most endpoints require JWT authentication. "
            "Use the `/api/auth/login/` endpoint to get your access tokens.\n\n"
        ),
        terms_of_service="https://www.shoptrack.com/terms/",
        contact=openapi.Contact(
            email="support@shoptrack.com",
            name="🛍️ ShopTrack Support Team",
            url="https://www.shoptrack.com/contact"
        ),
        license=openapi.License(
            name="MIT License",
            url="https://opensource.org/licenses/MIT"
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

class APIDocumentationHubView(TemplateView):
    """Main documentation hub page"""
    template_name = 'api-docs-hub.html'

urlpatterns = [
    # Admin - Use your custom admin site
    path("admin/", admin_site.urls),
    
    # API Endpoints
    path("api/auth/", include("apps.users.urls")),
    path("api/products/", include("apps.products.urls")),
    path("api/carts/", include("apps.carts.urls")),
    path("api/analytics/", include("apps.analytics.urls")),
    
    # Enhanced Documentation URLs
    path("docs/", APIDocumentationHubView.as_view(), name='docs-hub'),
    path("docs/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name='custom-swagger'),
    path("docs/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name='custom-redoc'),
    
    # Original documentation URLs (for compatibility)
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    
    # API Root
    path("", TemplateView.as_view(template_name='api-root.html'), name='api-root'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)