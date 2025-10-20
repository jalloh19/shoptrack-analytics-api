import pytest
from tests.factories import CartEventFactory, UserFactory  # Added UserFactory import

@pytest.mark.django_db
@pytest.mark.unit
class TestCartEventModel:
    def test_cart_event_creation(self):
        """Test basic cart event creation"""
        event = CartEventFactory()
        assert event.cart is not None
        assert event.user is not None
        assert event.event_type is not None
        assert event.timestamp is not None
        
    def test_cart_event_types(self):
        """Test cart event type choices"""
        event = CartEventFactory()
        valid_types = ['added', 'removed', 'updated', 'abandoned', 'purchased']
        assert event.event_type in valid_types
        
    def test_cart_event_quantity_changed(self):
        """Test quantity changed field"""
        event = CartEventFactory(quantity_changed=2)
        assert event.quantity_changed == 2
        
        event_negative = CartEventFactory(quantity_changed=-1)
        assert event_negative.quantity_changed == -1
        
    def test_cart_event_string_representation(self):
        """Test cart event string representation"""
        user = UserFactory(email='test@example.com')
        event = CartEventFactory(user=user, event_type='added')
        assert 'added' in str(event)
        assert 'test@example.com' in str(event)