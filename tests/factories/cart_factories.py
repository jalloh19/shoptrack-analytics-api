import factory
from faker import Faker
from apps.carts.models import Cart, CartItem
from tests.factories.user_factories import UserFactory
from tests.factories.product_factories import ProductFactory

fake = Faker()

class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart
    
    user = factory.SubFactory(UserFactory)
    status = 'active'

class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem
    
    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=5))