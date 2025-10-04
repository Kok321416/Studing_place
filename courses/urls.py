from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonDetailView, course_list, lesson_list

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    # API URLs
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    
    # HTML URLs
    path('html/courses/', course_list, name='course_list'),
    path('html/lessons/', lesson_list, name='lesson_list'),
]
