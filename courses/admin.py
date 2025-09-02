from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url


class LessonAdminForm(ModelForm):
    """Кастомная форма для модели Lesson с валидацией YouTube ссылок"""
    
    class Meta:
        model = Lesson
        fields = '__all__'
    
    def clean_video_link(self):
        """Валидация video_link поля в админке"""
        video_link = self.cleaned_data.get('video_link')
        if video_link:
            try:
                validate_youtube_url(video_link)
            except ValidationError as e:
                raise ValidationError(f"Ошибка валидации ссылки: {e}")
        return video_link


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at']
    list_filter = ['created_at', 'owner']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ['title', 'course', 'owner', 'video_link_status', 'created_at']
    list_filter = ['course', 'created_at', 'owner']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def video_link_status(self, obj):
        """Показывает статус валидации video_link"""
        if not obj.video_link:
            return "❌ Нет ссылки"
        
        try:
            validate_youtube_url(obj.video_link)
            return "✅ YouTube"
        except ValidationError:
            return "⚠️ Невалидная"
    
    video_link_status.short_description = "Статус ссылки"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'course']
    search_fields = ['user__email', 'course__title']
    readonly_fields = ['created_at']
