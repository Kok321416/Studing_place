from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class LessonListCreateView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


# HTML Views
def course_list(request):
    """Отображение списка курсов в HTML"""
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def lesson_list(request):
    """Отображение списка уроков в HTML"""
    lessons = Lesson.objects.all()
    return render(request, 'lessons/lesson_list.html', {'lessons': lessons})
