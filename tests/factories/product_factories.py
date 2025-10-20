import factory
from faker import Faker
from apps.products.models import Product

fake = Faker()

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    name = factory.LazyAttribute(lambda _: fake.unique.word().title())
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=200))
    price = factory.LazyAttribute(lambda _: fake.pydecimal(
        left_digits=5, right_digits=2, positive=True, min_value=1, max_value=999
    ))
    category = factory.LazyAttribute(lambda _: fake.random_element([
        'electronics', 'books', 'clothing', 'home', 'sports'
    ]))
    stock_quantity = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=1000))