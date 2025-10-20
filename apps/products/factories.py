import factory
from apps.products.models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    category = factory.Faker('word')
    stock_quantity = factory.Faker('random_int', min=10, max=100)