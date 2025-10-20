import factory
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.LazyAttribute(lambda _: fake.unique.email())
    username = factory.LazyAttribute(lambda _: fake.unique.user_name())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    role = 'customer'
    is_active = True
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to use create_user method for proper password handling"""
        password = kwargs.pop('password', 'testpass123')
        user = model_class.objects.create_user(*args, **kwargs)
        user.set_password(password)
        user.save()
        return user

class AdminUserFactory(UserFactory):
    role = 'admin'
    is_staff = True
    is_superuser = True