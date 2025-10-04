from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, UserRegistrationView, UserProfileView, UserListView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('list/', UserListView.as_view(), name='user-list'),
]
