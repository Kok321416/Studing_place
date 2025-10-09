"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('other_app/', Home.as_view(), name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from courses.views import course_list_view, lesson_list_view
from users.views import user_list_view, index_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Studing Place API",
        default_version="v1",
        description="API для платформы обучения с курсами и уроками",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@studingplace.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # HTML Pages
    path("", index_view, name="index"),  # Главная страница
    path("courses/", course_list_view, name="course_list"),  # HTML страница курсов
    path(
        "courses-with-payment/",
        lambda request: render(request, "courses_with_payment.html"),
        name="courses-with-payment",
    ),  # Курсы с оплатой
    path("lessons/", lesson_list_view, name="lesson_list"),  # HTML страница уроков
    path("users/", user_list_view, name="user_list"),  # HTML страница пользователей
    # Auth pages
    path("login/", lambda request: render(request, "login.html"), name="login"),
    path(
        "logout/",
        lambda request: render(request, "logout.html"),
        name="logout",
    ),
    # Admin and API
    path("admin/", admin.site.urls),
    # JWT Authentication endpoints (открытые для неавторизованных)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # API endpoints
    path("api/courses/", include("courses.urls")),
    path("api/users/", include("users.urls")),
    # Payment success/cancel pages
    path(
        "payment/success/",
        lambda request: render(request, "payment_success.html"),
        name="payment-success",
    ),
    path(
        "payment/cancel/",
        lambda request: render(request, "payment_cancel.html"),
        name="payment-cancel",
    ),
    # API Documentation
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
