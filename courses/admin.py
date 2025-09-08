from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm, inlineformset_factory
from django.utils.html import format_html
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


class LessonInline(admin.TabularInline):
    """Inline для добавления уроков прямо в курсе"""
    model = Lesson
    form = LessonAdminForm
    extra = 3  # Показывать 3 пустых формы для уроков
    fields = ['title', 'description', 'video_link', 'preview']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        """Оптимизация запросов"""
        return super().get_queryset(request).select_related('course', 'owner')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'price_display', 'lessons_count', 'created_at']
    list_filter = ['created_at', 'owner', 'price']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LessonInline]  # Добавляем inline для уроков
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'preview')
        }),
        ('Цена и владелец', {
            'fields': ('price', 'owner'),
            'description': 'Оставьте цену пустой для бесплатного курса'
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        """Красивое отображение цены"""
        if obj.price:
            return format_html(
                '<span style="color: #10B981; font-weight: bold;">{} ₽</span>',
                obj.price
            )
        return format_html(
            '<span style="color: #3B82F6; font-weight: bold;">БЕСПЛАТНО</span>'
        )
    price_display.short_description = 'Цена'
    
    def lessons_count(self, obj):
        """Количество уроков в курсе"""
        count = obj.lessons.count()
        return format_html(
            '<span style="color: #3B82F6; font-weight: bold;">{} уроков</span>',
            count
        )
    lessons_count.short_description = 'Уроки'
    
    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем владельца при создании"""
        if not change:  # Если это создание нового объекта
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ['title', 'course', 'owner', 'video_link_status', 'created_at']
    list_filter = ['course', 'created_at', 'owner']
    search_fields = ['title', 'description', 'video_link']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'preview')
        }),
        ('Видео', {
            'fields': ('video_link',),
            'description': 'Вставьте ссылку на YouTube видео (youtube.com или youtu.be)'
        }),
        ('Связи', {
            'fields': ('course', 'owner')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def video_link_status(self, obj):
        """Показывает статус валидации video_link"""
        if not obj.video_link:
            return format_html('<span style="color: #EF4444;">❌ Нет ссылки</span>')
        
        try:
            validate_youtube_url(obj.video_link)
            return format_html(
                '<span style="color: #10B981;">✅ YouTube</span><br>'
                '<a href="{}" target="_blank" style="font-size: 11px;">Открыть видео</a>',
                obj.video_link
            )
        except ValidationError:
            return format_html('<span style="color: #F59E0B;">⚠️ Невалидная ссылка</span>')
    
    video_link_status.short_description = "Статус ссылки"
    
    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем владельца при создании"""
        if not change:  # Если это создание нового объекта
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'course']
    search_fields = ['user__email', 'course__title']
    readonly_fields = ['created_at']
