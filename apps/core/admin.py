from django.contrib.admin import AdminSite
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

from apps.users.admin import CustomUserAdmin
from apps.users.models import User
from apps.products.models import Product
from apps.carts.models import Cart, CartItem
from apps.analytics.models import CartEvent


class ShopTrackAdminSite(AdminSite):
    site_header = "ShopTrack Analytics Administration"
    site_title = "ShopTrack Analytics Admin"
    index_title = "E-commerce Analytics Dashboard"

    def get_app_list(self, request):
        """
        Customize the app list ordering and labels
        """
        app_list = super().get_app_list(request)
        
        # Define custom ordering
        app_ordering = {
            'analytics': 0,
            'carts': 1,
            'products': 2,
            'users': 3,
            'auth': 4
        }
        
        # Reorder apps
        ordered_apps = []
        for app in app_list:
            app_label = app['app_label']
            order = app_ordering.get(app_label, 999)
            ordered_apps.append((order, app))
        
        ordered_apps.sort(key=lambda x: x[0])
        return [app for _, app in ordered_apps]

    def index(self, request, extra_context=None):
        """
        Add dashboard statistics to the admin index page
        """
        extra_context = extra_context or {}
        
        # Calculate statistics - using available fields
        extra_context['total_users'] = User.objects.count()
        extra_context['active_products'] = Product.objects.count()  # All products
        extra_context['active_carts'] = Cart.objects.filter(status='active').count()
        
        # Stock information
        extra_context['in_stock_products'] = Product.objects.filter(stock_quantity__gt=0).count()
        extra_context['out_of_stock_products'] = Product.objects.filter(stock_quantity=0).count()
        
        # Abandonment rate calculation
        total_carts = Cart.objects.count()
        completed_carts = Cart.objects.filter(status='completed').count()
        if total_carts > 0:
            extra_context['abandonment_rate'] = round(
                ((total_carts - completed_carts) / total_carts) * 100, 1
            )
        else:
            extra_context['abandonment_rate'] = 0
        
        return super().index(request, extra_context)


# Create custom admin site instance
admin_site = ShopTrackAdminSite(name='admin')


# Register models with the custom admin site
admin_site.register(User, CustomUserAdmin)
admin_site.register(Product)
admin_site.register(Cart)
admin_site.register(CartItem)
admin_site.register(CartEvent)
admin_site.register(Group)