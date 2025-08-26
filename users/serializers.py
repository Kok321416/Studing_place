from rest_framework import serializers
from .models import Payment
from courses.serializers import CourseSerializer, LessonSerializer

class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
