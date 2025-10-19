from django.db import models
import uuid
from django.conf import settings

class CartEvent(models.Model):
    EVENT_TYPES = [
        ('added', 'Item Added'),
        ('removed', 'Item Removed'), 
        ('updated', 'Item Updated'),
        ('abandoned', 'Cart Abandoned'),
        ('purchased', 'Cart Purchased'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey('carts.Cart', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    quantity_changed = models.IntegerField(default=0)  # Positive for add, negative for remove
    timestamp = models.DateTimeField(auto_now_add=True)
    session_duration_seconds = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.event_type} - {self.user.email} - {self.timestamp}"

    class Meta:
        db_table = 'cart_events'
        verbose_name = 'Cart Event'
        verbose_name_plural = 'Cart Events'
        ordering = ['-timestamp']