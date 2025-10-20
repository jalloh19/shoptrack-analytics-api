import factory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        # Prevent factory-boy from trying to create a user with the same email twice
        django_get_or_create = ('email',)

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    role = 'customer'  # Default role is 'customer'

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or 'default_password123'
        if create:
            self.set_password(password)