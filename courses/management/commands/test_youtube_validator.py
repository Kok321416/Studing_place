from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from courses.validators import validate_youtube_url


class Command(BaseCommand):
    help = 'Тестирует валидатор YouTube ссылок с примерами URL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Конкретный URL для тестирования'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Запустить тест всех примеров URL'
        )

    def handle(self, *args, **options):
        """Тестирует валидатор YouTube ссылок"""
        
        if options['url']:
            # Тестируем конкретный URL
            self.test_single_url(options['url'])
        else:
            # Тестируем все примеры
            self.test_all_examples()

    def test_single_url(self, url):
        """Тестирует один конкретный URL"""
        self.stdout.write(f"\n🔍 Тестирование URL: {url}")
        self.stdout.write("-" * 50)
        
        try:
            validate_youtube_url(url)
            self.stdout.write(
                self.style.SUCCESS(f"✅ URL прошел валидацию: {url}")
            )
        except ValidationError as e:
            self.stdout.write(
                self.style.ERROR(f"❌ URL отклонен: {e}")
            )

    def test_all_examples(self):
        """Тестирует все примеры URL"""
        self.stdout.write(
            self.style.SUCCESS("🧪 Запуск тестирования YouTube валидатора")
        )
        self.stdout.write("=" * 60)
        
        # Валидные YouTube ссылки
        valid_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtube.com/watch?v=dQw4w9WgXcQ', 
            'https://youtu.be/dQw4w9WgXcQ',
            'https://m.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://music.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://gaming.youtube.com/watch?v=dQw4w9WgXcQ',
        ]
        
        # Невалидные ссылки
        invalid_urls = [
            'https://vimeo.com/123456789',
            'https://rutube.ru/video/123/',
            'https://stepik.org/course/123/',
            'https://example.com/video.mp4',
            'https://dailymotion.com/video/123',
            'https://twitch.tv/username',
            'http://youtube.com/watch?v=123',  # HTTP вместо HTTPS
        ]
        
        # Тестируем валидные URL
        self.stdout.write("\n✅ Тестирование ВАЛИДНЫХ YouTube ссылок:")
        self.stdout.write("-" * 40)
        
        valid_passed = 0
        for url in valid_urls:
            try:
                validate_youtube_url(url)
                self.stdout.write(f"  ✅ {url}")
                valid_passed += 1
            except ValidationError as e:
                self.stdout.write(
                    self.style.ERROR(f"  ❌ ОШИБКА: {url} - {e}")
                )
        
        # Тестируем невалидные URL
        self.stdout.write("\n❌ Тестирование НЕВАЛИДНЫХ ссылок:")
        self.stdout.write("-" * 40)
        
        invalid_blocked = 0
        for url in invalid_urls:
            try:
                validate_youtube_url(url)
                self.stdout.write(
                    self.style.ERROR(f"  ⚠️  ПРОПУЩЕН: {url}")
                )
            except ValidationError as e:
                self.stdout.write(f"  ✅ ЗАБЛОКИРОВАН: {url}")
                self.stdout.write(f"     Причина: {e}")
                invalid_blocked += 1
        
        # Итоговая статистика
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(
            self.style.SUCCESS(
                f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:"
                f"\n   Валидных URL прошло: {valid_passed}/{len(valid_urls)}"
                f"\n   Невалидных URL заблокировано: {invalid_blocked}/{len(invalid_urls)}"
                f"\n   Общий результат: {'✅ УСПЕШНО' if valid_passed == len(valid_urls) and invalid_blocked == len(invalid_urls) else '❌ ЕСТЬ ПРОБЛЕМЫ'}"
            )
        )
        
        # Инструкции по использованию
        self.stdout.write(
            self.style.SUCCESS(
                f"\n💡 ИСПОЛЬЗОВАНИЕ:"
                f"\n   python manage.py test_youtube_validator --all"
                f"\n   python manage.py test_youtube_validator --url 'https://youtube.com/watch?v=123'"
            )
        )
