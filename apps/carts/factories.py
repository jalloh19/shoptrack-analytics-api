import factory
from apps.carts.models import Cart, CartItem
from apps.users.factories import UserFactory
from apps.products.factories import ProductFactory

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
    quantity = factory.Faker('random_int', min=1, max=5)