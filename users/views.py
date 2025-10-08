from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, Payment
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserListSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
    PaymentResponseSerializer,
)
from .filters import PaymentFilter
from .stripe_service import create_payment_flow, get_payment_status
from courses.models import Course, Lesson

UserModel = get_user_model()


# HTML Views
def user_list_view(request):
    """Отображение HTML страницы пользователей"""
    return render(request, "users.html")


def index_view(request):
    """Отображение главной страницы"""
    return render(request, "index.html")


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


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с платежами"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]  # По умолчанию сортировка по дате (новые сначала)

    def get_queryset(self):
        """Возвращаем только платежи текущего пользователя"""
        return Payment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от действия"""
        if self.action == "create":
            return PaymentCreateSerializer
        elif self.action in ["list", "retrieve"]:
            return PaymentResponseSerializer
        return PaymentSerializer

    @swagger_auto_schema(
        operation_summary="Создать платеж",
        operation_description="Создает новый платеж для курса или урока через Stripe",
        request_body=PaymentCreateSerializer,
        responses={
            201: PaymentResponseSerializer,
            400: "Ошибка валидации данных",
            404: "Курс или урок не найден",
        },
    )
    def create(self, request, *args, **kwargs):
        """Создание платежа через Stripe"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_id = serializer.validated_data.get("course_id")
        lesson_id = serializer.validated_data.get("lesson_id")
        amount = serializer.validated_data.get("amount")

        try:
            if course_id:
                course = get_object_or_404(Course, id=course_id)
                if not course.price:
                    return Response(
                        {"error": "У курса не установлена цена"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                amount = course.price
                success_url = request.build_absolute_uri(reverse("payment-success"))
                cancel_url = request.build_absolute_uri(reverse("payment-cancel"))

                # Создаем процесс оплаты через Stripe
                stripe_data = create_payment_flow(
                    course, request.user, success_url, cancel_url
                )

                # Создаем платеж в нашей системе
                payment = Payment.objects.create(
                    user=request.user,
                    course=course,
                    amount=amount,
                    payment_method="stripe",
                    stripe_product_id=stripe_data["product_id"],
                    stripe_price_id=stripe_data["price_id"],
                    stripe_session_id=stripe_data["session_id"],
                    payment_url=stripe_data["payment_url"],
                )

            elif lesson_id:
                lesson = get_object_or_404(Lesson, id=lesson_id)
                if not lesson.course.price:
                    return Response(
                        {"error": "У курса урока не установлена цена"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                amount = lesson.course.price
                success_url = request.build_absolute_uri(reverse("payment-success"))
                cancel_url = request.build_absolute_uri(reverse("payment-cancel"))

                # Создаем процесс оплаты через Stripe
                stripe_data = create_payment_flow(
                    lesson.course, request.user, success_url, cancel_url
                )

                # Создаем платеж в нашей системе
                payment = Payment.objects.create(
                    user=request.user,
                    lesson=lesson,
                    course=lesson.course,
                    amount=amount,
                    payment_method="stripe",
                    stripe_product_id=stripe_data["product_id"],
                    stripe_price_id=stripe_data["price_id"],
                    stripe_session_id=stripe_data["session_id"],
                    payment_url=stripe_data["payment_url"],
                )

            response_serializer = PaymentResponseSerializer(payment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Ошибка создания платежа: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Проверить статус платежа",
        operation_description="Проверяет статус платежа в Stripe",
        responses={
            200: openapi.Response(
                description="Статус платежа",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Статус платежа"
                        ),
                        "payment_status": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Статус в Stripe"
                        ),
                    },
                ),
            ),
            404: "Платеж не найден",
        },
    )
    @action(detail=True, methods=["get"])
    def check_status(self, request, pk=None):
        """Проверка статуса платежа"""
        payment = self.get_object()

        if not payment.stripe_session_id:
            return Response(
                {"error": "У платежа нет Stripe сессии"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            stripe_status = get_payment_status(payment.stripe_session_id)
            payment.status = stripe_status
            payment.save()

            return Response(
                {
                    "status": payment.status,
                    "status_display": payment.get_status_display(),
                    "payment_status": stripe_status,
                }
            )
        except Exception as e:
            return Response(
                {"error": f"Ошибка проверки статуса: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
