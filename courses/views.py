from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModeratorOrOwnerForModify, IsOwner, IsModeratorOrOwner

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
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
            permission_classes = [IsModeratorOrOwnerForModify]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        elif self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]

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
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'description', 'course']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['-created_at']

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
    permission_classes = [IsModeratorOrOwnerForModify]

    def get_queryset(self):
        """Фильтруем queryset в зависимости от роли пользователя"""
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

# HTML views для отображения страниц
def course_list(request):
    """Отображение списка курсов для HTML страницы"""
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def lesson_list(request):
    """Отображение списка уроков для HTML страницы"""
    lessons = Lesson.objects.all()
    return render(request, 'lessons/lesson_list.html', {'lessons': lessons})
