import factory
from faker import Faker
from apps.analytics.models import CartEvent
from tests.factories.cart_factories import CartFactory
from tests.factories.product_factories import ProductFactory

fake = Faker()

class CartEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartEvent
    
    cart = factory.SubFactory(CartFactory)
    user = factory.LazyAttribute(lambda obj: obj.cart.user)
    product = factory.SubFactory(ProductFactory)
    event_type = factory.LazyAttribute(lambda _: fake.random_element([
        'added', 'removed', 'updated', 'abandoned', 'purchased'
    ]))
    quantity_changed = factory.LazyAttribute(lambda _: fake.random_int(min=-5, max=5))
    session_duration_seconds = factory.LazyAttribute(
        lambda _: fake.random_int(min=60, max=3600)
    )