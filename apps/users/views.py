from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer,
    CustomTokenObtainPairSerializer
)

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint
    Public access - no authentication required
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile retrieval and update
    Authenticated users only
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view with user role in token
    """
    serializer_class = CustomTokenObtainPairSerializer