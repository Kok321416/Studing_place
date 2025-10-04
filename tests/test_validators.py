"""
Тестовый файл для проверки валидаторов YouTube ссылок.
Запуск: python manage.py test tests.test_validators
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from courses.validators import validate_youtube_url, YouTubeURLValidator


class YouTubeValidatorTest(TestCase):
    """Тесты для валидатора YouTube ссылок"""
    
    def test_valid_youtube_urls(self):
        """Тест допустимых YouTube ссылок"""
        valid_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtu.be/dQw4w9WgXcQ',
            'https://m.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://music.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://gaming.youtube.com/watch?v=dQw4w9WgXcQ',
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                try:
                    validate_youtube_url(url)
                except ValidationError:
                    self.fail(f"Валидная YouTube ссылка отклонена: {url}")
    
    def test_invalid_urls(self):
        """Тест недопустимых ссылок"""
        invalid_urls = [
            'https://vimeo.com/123456789',
            'https://rutube.ru/video/123/',
            'https://stepik.org/course/123/',
            'https://example.com/video.mp4',
            'https://dailymotion.com/video/123',
            'https://twitch.tv/username',
            'https://facebook.com/video/123',
        ]
        
        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises(ValidationError):
                    validate_youtube_url(url)
    
    def test_http_urls_rejected(self):
        """Тест отклонения HTTP ссылок (требуется HTTPS)"""
        http_urls = [
            'http://youtube.com/watch?v=dQw4w9WgXcQ',
            'http://www.youtube.com/watch?v=dQw4w9WgXcQ',
        ]
        
        for url in http_urls:
            with self.subTest(url=url):
                with self.assertRaises(ValidationError):
                    validate_youtube_url(url)
    
    def test_empty_url(self):
        """Тест пустых значений - должны пропускаться без ошибок"""
        empty_values = [None, '', '   ']
        
        for value in empty_values:
            with self.subTest(value=repr(value)):
                try:
                    result = validate_youtube_url(value)
                    # Пустые значения должны возвращать None (пропускаются)
                    self.assertIsNone(result, f"Пустое значение должно возвращать None: {repr(value)}")
                except ValidationError:
                    self.fail(f"Пустое значение должно быть пропущено без ошибки: {repr(value)}")
    
    def test_class_validator(self):
        """Тест класса-валидатора"""
        validator = YouTubeURLValidator(field='video_link')
        
        # Валидная ссылка
        try:
            validator('https://youtube.com/watch?v=dQw4w9WgXcQ')
        except ValidationError:
            self.fail("Класс-валидатор отклонил валидную ссылку")
        
        # Невалидная ссылка
        with self.assertRaises(ValidationError):
            validator('https://vimeo.com/123456789')


class ValidationErrorMessagesTest(TestCase):
    """Тесты сообщений об ошибках"""
    
    def test_forbidden_domain_message(self):
        """Тест сообщения для запрещенного домена"""
        with self.assertRaises(ValidationError) as cm:
            validate_youtube_url('https://vimeo.com/123')
        
        self.assertIn('Разрешены только ссылки на YouTube', str(cm.exception))
    
    def test_http_protocol_message(self):
        """Тест сообщения для HTTP протокола"""
        with self.assertRaises(ValidationError) as cm:
            validate_youtube_url('http://youtube.com/watch?v=123')
        
        self.assertIn('HTTPS протокол', str(cm.exception))
