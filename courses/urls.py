from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonDetailView, course_list_view, lesson_list_view, SubscriptionAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    
    # Subscription API
    path('subscription/', SubscriptionAPIView.as_view(), name='course-subscription'),
    
    # HTML views
    path('html/courses/', course_list_view, name='course_list'),
    path('html/lessons/', lesson_list_view, name='lesson_list'),
]
