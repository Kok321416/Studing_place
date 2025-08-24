from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'phone', 'city', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'city']
    search_fields = ['email', 'phone']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'city', 'avatar')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'city', 'avatar')}),
    )
    
    ordering = ['email']  # Заменяем username на email
