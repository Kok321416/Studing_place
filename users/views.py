from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import User
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserListSerializer

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """Регистрация пользователей - доступна для неавторизованных"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Профиль пользователя - доступен только авторизованным"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    """Список пользователей - доступен только авторизованным"""
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
