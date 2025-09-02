from django.core.exceptions import ValidationError
import re
from urllib.parse import urlparse


def validate_youtube_url(value):
    """
    Валидатор для проверки, что ссылка ведет только на YouTube.
    Разрешены только ссылки на youtube.com и youtu.be домены.
    """
    if not value:
        return  # Пустые значения пропускаем (если поле не обязательное)
    
    try:
        # Парсим URL
        parsed_url = urlparse(value)
        domain = parsed_url.netloc.lower()
        
        # Убираем www. префикс для унификации
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Список разрешенных доменов YouTube
        allowed_domains = [
            'youtube.com',
            'youtu.be',
            'm.youtube.com',
            'music.youtube.com',
            'gaming.youtube.com'
        ]
        
        # Проверяем, что домен в списке разрешенных
        if domain not in allowed_domains and not domain.endswith('.youtube.com'):
            raise ValidationError(
                'Разрешены только ссылки на YouTube. '
                'Ссылки на сторонние ресурсы запрещены.',
                code='invalid_url'
            )
            
        # Дополнительная проверка: URL должен быть HTTPS для безопасности
        if parsed_url.scheme != 'https':
            raise ValidationError(
                'Ссылка должна использовать HTTPS протокол.',
                code='insecure_url'
            )
            
    except Exception as e:
        if isinstance(e, ValidationError):
            raise e
        raise ValidationError(
            'Некорректный формат URL. Проверьте правильность ссылки.',
            code='invalid_format'
        )


class YouTubeURLValidator:
    """
    Класс-валидатор для проверки YouTube ссылок.
    Альтернативная реализация в виде класса.
    """
    def __init__(self, field=None):
        self.field = field
    
    def __call__(self, value):
        """Вызывается при валидации"""
        validate_youtube_url(value)
    
    def deconstruct(self):
        """Необходимо для миграций Django"""
        return (
            'courses.validators.YouTubeURLValidator',
            (),
            {'field': self.field}
        )