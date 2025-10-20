import factory
from apps.analytics.models import CartEvent
from apps.carts.factories import CartFactory
from apps.users.factories import UserFactory
from apps.products.factories import ProductFactory

class CartEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartEvent

    cart = factory.SubFactory(CartFactory)
    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    event_type = factory.Iterator(['added', 'removed', 'updated', 'purchased', 'abandoned'])
    quantity_changed = factory.Faker('random_int', min=-5, max=5)
    session_duration_seconds = factory.Faker('random_int', min=10, max=300)