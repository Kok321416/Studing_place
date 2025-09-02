from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import User, Payment
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserListSerializer, PaymentSerializer
from .filters import PaymentFilter

UserModel = get_user_model()

# HTML Views
def user_list_view(request):
    """Отображение HTML страницы пользователей"""
    return render(request, 'users.html')

def index_view(request):
    """Отображение главной страницы"""
    return render(request, 'index.html')

# API Views
class UserRegistrationView(generics.CreateAPIView):
    """Регистрация пользователей - доступна для неавторизованных"""
    queryset = UserModel.objects.all()
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
    queryset = UserModel.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # По умолчанию сортировка по дате (новые сначала)
