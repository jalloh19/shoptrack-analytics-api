import pytest
from django.core.exceptions import ValidationError
from tests.factories import UserFactory, AdminUserFactory

@pytest.mark.django_db
@pytest.mark.unit
class TestUserModel:
    def test_user_creation(self):
        """Test basic user creation"""
        user = UserFactory()
        assert user.email is not None
        assert user.role == 'customer'
        assert user.check_password('testpass123')
        
    def test_admin_user_creation(self):
        """Test admin user creation"""
        admin = AdminUserFactory()
        assert admin.role == 'admin'
        assert admin.is_staff is True
        
    def test_user_string_representation(self):
        """Test user string representation"""
        user = UserFactory(email='test@example.com')
        assert str(user) == 'test@example.com'
        
    def test_user_required_fields(self):
        """Test user required fields"""
        user = UserFactory.build()
        assert hasattr(user, 'email')
        assert hasattr(user, 'username')
        assert hasattr(user, 'role')