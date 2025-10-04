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
    """HTML страница со списком курсов"""
    courses = Course.objects.all()
    context = {
        'courses': courses,
        'courses_count': courses.count()
    }
    return render(request, 'courses/course_list.html', context)

def lesson_list(request):
    """HTML страница со списком уроков"""
    lessons = Lesson.objects.all()
    context = {
        'lessons': lessons,
        'lessons_count': lessons.count()
    }
    return render(request, 'lessons/lesson_list.html', context)
