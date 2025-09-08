from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModeratorOrOwnerForModify, IsOwner, IsModeratorOrOwner, IsModerator
from .paginators import CoursesPagination, LessonsPagination

# Create your views here.

# HTML Views
def course_list_view(request):
    """Отображение HTML страницы курсов"""
    return render(request, 'courses.html')

def lesson_list_view(request):
    """Отображение HTML страницы уроков"""
    return render(request, 'lessons.html')

# API Views
class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.
    
    Позволяет создавать, просматривать, обновлять и удалять курсы.
    Модераторы могут редактировать все курсы, но не могут создавать или удалять.
    Обычные пользователи могут создавать курсы и управлять только своими.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CoursesPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'description']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        Динамически назначаем разрешения в зависимости от действия
        """
        if self.action in ['update', 'partial_update']:
            # Модераторы и владельцы могут редактировать
            permission_classes = [IsAuthenticated, IsModeratorOrOwnerForModify]
        elif self.action == 'destroy':
            # Только владельцы могут удалять (модераторы НЕ могут)
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == 'create':
            # Только обычные пользователи могут создавать (модераторы НЕ могут)
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['list', 'retrieve']:
            # Все авторизованные могут просматривать
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        operation_summary="Создать курс",
        operation_description="Создает новый курс. Доступно только обычным пользователям.",
        responses={
            201: CourseSerializer,
            400: "Ошибка валидации данных",
            403: "Доступ запрещен"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Получить список курсов",
        operation_description="Возвращает список курсов с пагинацией и фильтрацией",
        responses={
            200: CourseSerializer(many=True),
            401: "Не авторизован"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Получить курс",
        operation_description="Возвращает детальную информацию о курсе",
        responses={
            200: CourseSerializer,
            404: "Курс не найден"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Обновить курс",
        operation_description="Обновляет информацию о курсе. Доступно владельцу или модератору.",
        responses={
            200: CourseSerializer,
            400: "Ошибка валидации данных",
            403: "Доступ запрещен",
            404: "Курс не найден"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Частично обновить курс",
        operation_description="Частично обновляет информацию о курсе. Доступно владельцу или модератору.",
        responses={
            200: CourseSerializer,
            400: "Ошибка валидации данных",
            403: "Доступ запрещен",
            404: "Курс не найден"
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Удалить курс",
        operation_description="Удаляет курс. Доступно только владельцу.",
        responses={
            204: "Курс удален",
            403: "Доступ запрещен",
            404: "Курс не найден"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Автоматически назначаем владельца при создании курса"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Фильтруем queryset в зависимости от роли пользователя"""
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

class LessonListCreateView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'description', 'course']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Динамически назначаем разрешения в зависимости от действия"""
        if self.request.method == 'POST':
            # Только обычные пользователи могут создавать (модераторы НЕ могут)
            permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            # Все авторизованные могут просматривать список
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Автоматически назначаем владельца при создании урока"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Фильтруем queryset в зависимости от роли пользователя"""
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

class LessonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Динамически назначаем разрешения в зависимости от действия"""
        if self.request.method == 'DELETE':
            # Только владельцы могут удалять (модераторы НЕ могут)
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.request.method in ['PUT', 'PATCH']:
            # Модераторы и владельцы могут редактировать
            permission_classes = [IsAuthenticated, IsModeratorOrOwnerForModify]
        else:
            # Все авторизованные могут просматривать
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Фильтруем queryset в зависимости от роли пользователя"""
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class SubscriptionAPIView(APIView):
    """API для управления подписками на курсы"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Переключение подписки: создание или удаление"""
        user = request.user
        course_id = request.data.get('course_id')
        
        if not course_id:
            return Response(
                {"error": "Не указан ID курса"}, 
                status=400
            )
        
        course_item = get_object_or_404(Course, id=course_id)
        
        # Проверяем существующую подписку
        subs_item = Subscription.objects.filter(
            user=user, 
            course=course_item
        )
        
        # Если подписка есть - удаляем
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
            subscribed = False
        # Если подписки нет - создаем
        else:
            Subscription.objects.create(
                user=user,
                course=course_item
            )
            message = 'подписка добавлена'
            subscribed = True
        
        return Response({
            "message": message,
            "subscribed": subscribed,
            "course_id": course_id,
            "course_title": course_item.title
        })
