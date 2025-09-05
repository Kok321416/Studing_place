from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from courses.models import Course, Lesson, Subscription

User = get_user_model()


class AllEndpointsTestCase(APITestCase):
    """Комплексные тесты всех эндпоинтов проекта"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем группы
        self.moderators_group = Group.objects.create(name='Модераторы')
        self.users_group = Group.objects.create(name='Пользователи')
        
        # Создаем пользователей
        self.owner_user = User.objects.create_user(
            email='owner@test.com',
            password='testpass123',
            first_name='Owner',
            last_name='User',
            phone='+1234567890',
            city='Moscow'
        )
        
        self.moderator_user = User.objects.create_user(
            email='moderator@test.com',
            password='testpass123',
            first_name='Moderator',
            last_name='User',
            phone='+1234567891',
            city='Moscow'
        )
        self.moderator_user.groups.add(self.moderators_group)
        
        self.regular_user = User.objects.create_user(
            email='regular@test.com',
            password='testpass123',
            first_name='Regular',
            last_name='User',
            phone='+1234567892',
            city='Moscow'
        )
        
        # Создаем тестовые данные
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            owner=self.owner_user
        )
        
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание тестового урока',
            video_link='https://youtube.com/watch?v=test123',
            course=self.course,
            owner=self.owner_user
        )

    def get_jwt_token(self, user):
        """Получение JWT токена для пользователя"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_jwt_token_obtain(self):
        """Тест получения JWT токена"""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'owner@test.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_token_refresh(self):
        """Тест обновления JWT токена"""
        # Сначала получаем токен
        refresh = RefreshToken.for_user(self.owner_user)
        url = reverse('token_refresh')
        data = {'refresh': str(refresh)}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_registration(self):
        """Тест регистрации пользователя"""
        url = reverse('user-registration')
        data = {
            'email': 'newuser@test.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '+1234567893',
            'city': 'Moscow'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@test.com').exists())

    def test_user_profile_retrieve(self):
        """Тест получения профиля пользователя"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('user-profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'owner@test.com')

    def test_user_profile_update(self):
        """Тест обновления профиля пользователя"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('user-profile')
        data = {'first_name': 'Updated Name'}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated Name')

    def test_user_list(self):
        """Тест получения списка пользователей"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('user-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_course_list_endpoint(self):
        """Тест эндпоинта списка курсов"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('course-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

    def test_course_detail_endpoint(self):
        """Тест эндпоинта детального просмотра курса"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('course-detail', kwargs={'pk': self.course.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовый курс')
        self.assertIn('is_subscribed', response.data)

    def test_course_create_endpoint(self):
        """Тест эндпоинта создания курса"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('course-list')
        data = {
            'title': 'Новый курс',
            'description': 'Описание нового курса'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_course_update_endpoint(self):
        """Тест эндпоинта обновления курса"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('course-detail', kwargs={'pk': self.course.pk})
        data = {'title': 'Обновленный курс'}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Обновленный курс')

    def test_course_delete_endpoint(self):
        """Тест эндпоинта удаления курса"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('course-detail', kwargs={'pk': self.course.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_lesson_list_endpoint(self):
        """Тест эндпоинта списка уроков"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('lesson-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

    def test_lesson_create_endpoint(self):
        """Тест эндпоинта создания урока"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('lesson-list-create')
        data = {
            'title': 'Новый урок',
            'description': 'Описание нового урока',
            'video_link': 'https://youtube.com/watch?v=new123',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_detail_endpoint(self):
        """Тест эндпоинта детального просмотра урока"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовый урок')

    def test_lesson_update_endpoint(self):
        """Тест эндпоинта обновления урока"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.pk})
        data = {'title': 'Обновленный урок'}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Обновленный урок')

    def test_lesson_delete_endpoint(self):
        """Тест эндпоинта удаления урока"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscription_endpoint(self):
        """Тест эндпоинта подписки на курс"""
        token = self.get_jwt_token(self.owner_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('course-subscription')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('subscribed', response.data)

    def test_unauthorized_access(self):
        """Тест доступа без авторизации"""
        # Тестируем несколько защищенных эндпоинтов
        endpoints = [
            reverse('course-list'),
            reverse('lesson-list-create'),
            reverse('user-profile'),
            reverse('user-list'),
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_jwt_token(self):
        """Тест с невалидным JWT токеном"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        
        url = reverse('course-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expired_jwt_token(self):
        """Тест с истекшим JWT токеном"""
        # Создаем токен с коротким временем жизни
        from datetime import timedelta
        from rest_framework_simplejwt.settings import api_settings
        
        # Временно изменяем время жизни токена
        original_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
        api_settings.ACCESS_TOKEN_LIFETIME = timedelta(seconds=1)
        
        try:
            token = self.get_jwt_token(self.owner_user)
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
            
            # Ждем истечения токена
            import time
            time.sleep(2)
            
            url = reverse('course-list')
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        finally:
            # Восстанавливаем оригинальное время жизни
            api_settings.ACCESS_TOKEN_LIFETIME = original_lifetime


class HTMLViewsTestCase(TestCase):
    """Тесты HTML представлений"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            phone='+1234567890',
            city='Moscow'
        )
        
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание курса',
            owner=self.user
        )
        
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание урока',
            video_link='https://youtube.com/watch?v=test123',
            course=self.course,
            owner=self.user
        )

    def test_index_view(self):
        """Тест главной страницы"""
        url = reverse('index')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Главная страница')

    def test_course_list_view(self):
        """Тест HTML страницы списка курсов"""
        url = reverse('course_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список курсов')

    def test_lesson_list_view(self):
        """Тест HTML страницы списка уроков"""
        url = reverse('lesson_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список уроков')

    def test_user_list_view(self):
        """Тест HTML страницы списка пользователей"""
        url = reverse('user_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список пользователей')


class ValidationTestCase(APITestCase):
    """Тесты валидации данных"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            phone='+1234567890',
            city='Moscow'
        )
        
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание курса',
            owner=self.user
        )

    def test_youtube_url_validation_valid_urls(self):
        """Тест валидации валидных YouTube URL"""
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        valid_urls = [
            'https://youtube.com/watch?v=test123',
            'https://www.youtube.com/watch?v=test123',
            'https://youtu.be/test123',
            'https://m.youtube.com/watch?v=test123',
            'https://music.youtube.com/watch?v=test123',
            'https://gaming.youtube.com/watch?v=test123',
        ]
        
        url = reverse('lesson-list-create')
        
        for video_url in valid_urls:
            data = {
                'title': f'Урок с {video_url}',
                'description': 'Описание',
                'video_link': video_url,
                'course': self.course.id
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, 
                           f'URL {video_url} должен быть валидным')

    def test_youtube_url_validation_invalid_urls(self):
        """Тест валидации невалидных URL"""
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        invalid_urls = [
            'https://vimeo.com/123456789',
            'https://example.com/video',
            'http://youtube.com/watch?v=test123',  # HTTP вместо HTTPS
            'https://facebook.com/video',
            'https://instagram.com/video',
            'not_a_url',
            '',
        ]
        
        url = reverse('lesson-list-create')
        
        for video_url in invalid_urls:
            data = {
                'title': f'Урок с {video_url}',
                'description': 'Описание',
                'video_link': video_url,
                'course': self.course.id
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 
                           f'URL {video_url} должен быть невалидным')
            self.assertIn('video_link', response.data)

    def test_required_fields_validation(self):
        """Тест валидации обязательных полей"""
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('lesson-list-create')
        
        # Тест без обязательных полей
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Тест без title
        data = {
            'description': 'Описание',
            'video_link': 'https://youtube.com/watch?v=test123',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        
        # Тест без course
        data = {
            'title': 'Урок',
            'description': 'Описание',
            'video_link': 'https://youtube.com/watch?v=test123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('course', response.data)
