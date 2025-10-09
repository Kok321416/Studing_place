from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from courses.models import Course, Lesson, Subscription

User = get_user_model()


class CoursesCRUDTestCase(APITestCase):
    """Тесты CRUD операций для курсов"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем группы
        self.moderators_group = Group.objects.create(name="Модераторы")
        self.users_group = Group.objects.create(name="Пользователи")

        # Создаем пользователей
        self.owner_user = User.objects.create_user(
            email="owner@test.com",
            password="testpass123",
            first_name="Owner",
            last_name="User",
            phone="+1234567890",
            city="Moscow",
        )

        self.moderator_user = User.objects.create_user(
            email="moderator@test.com",
            password="testpass123",
            first_name="Moderator",
            last_name="User",
            phone="+1234567891",
            city="Moscow",
        )
        self.moderator_user.groups.add(self.moderators_group)

        self.regular_user = User.objects.create_user(
            email="regular@test.com",
            password="testpass123",
            first_name="Regular",
            last_name="User",
            phone="+1234567892",
            city="Moscow",
        )

        # Создаем тестовый курс
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание тестового курса",
            owner=self.owner_user,
        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Описание тестового урока",
            video_link="https://youtube.com/watch?v=test123",
            course=self.course,
            owner=self.owner_user,
        )

    def test_course_list_authenticated(self):
        """Тест получения списка курсов авторизованным пользователем"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("course-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)  # Пагинация
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_course_list_unauthenticated(self):
        """Тест получения списка курсов неавторизованным пользователем"""
        url = reverse("course-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_create_by_owner(self):
        """Тест создания курса владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("course-list")
        data = {"title": "Новый курс", "description": "Описание нового курса"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        new_course = Course.objects.get(title="Новый курс")
        self.assertEqual(new_course.owner, self.owner_user)

    def test_course_create_by_moderator_forbidden(self):
        """Тест создания курса модератором (должно быть запрещено)"""
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("course-list")
        data = {
            "title": "Курс от модератора",
            "description": "Описание курса от модератора",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_update_by_owner(self):
        """Тест обновления курса владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        data = {
            "title": "Обновленный курс",
            "description": "Обновленное описание",
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Обновленный курс")

    def test_course_update_by_moderator(self):
        """Тест обновления курса модератором"""
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        data = {
            "title": "Курс обновлен модератором",
            "description": "Описание обновлено модератором",
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Курс обновлен модератором")

    def test_course_delete_by_owner(self):
        """Тест удаления курса владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_course_delete_by_moderator_forbidden(self):
        """Тест удаления курса модератором (должно быть запрещено)"""
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 1)  # Курс не удален

    def test_course_delete_by_other_user_forbidden(self):
        """Тест удаления курса другим пользователем (должно быть запрещено)"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 1)  # Курс не удален


class LessonsCRUDTestCase(APITestCase):
    """Тесты CRUD операций для уроков"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем группы
        self.moderators_group = Group.objects.create(name="Модераторы")

        # Создаем пользователей
        self.owner_user = User.objects.create_user(
            email="owner@test.com",
            password="testpass123",
            first_name="Owner",
            last_name="User",
            phone="+1234567890",
            city="Moscow",
        )

        self.moderator_user = User.objects.create_user(
            email="moderator@test.com",
            password="testpass123",
            first_name="Moderator",
            last_name="User",
            phone="+1234567891",
            city="Moscow",
        )
        self.moderator_user.groups.add(self.moderators_group)

        self.regular_user = User.objects.create_user(
            email="regular@test.com",
            password="testpass123",
            first_name="Regular",
            last_name="User",
            phone="+1234567892",
            city="Moscow",
        )

        # Создаем тестовый курс
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание тестового курса",
            owner=self.owner_user,
        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Описание тестового урока",
            video_link="https://youtube.com/watch?v=test123",
            course=self.course,
            owner=self.owner_user,
        )

    def test_lesson_list_with_pagination(self):
        """Тест получения списка уроков с пагинацией"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lesson-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)

    def test_lesson_create_by_owner(self):
        """Тест создания урока владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lesson-list-create")
        data = {
            "title": "Новый урок",
            "description": "Описание нового урока",
            "video_link": "https://youtube.com/watch?v=new123",
            "course": self.course.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        new_lesson = Lesson.objects.get(title="Новый урок")
        self.assertEqual(new_lesson.owner, self.owner_user)

    def test_lesson_create_by_moderator_forbidden(self):
        """Тест создания урока модератором (должно быть запрещено)"""
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lesson-list-create")
        data = {
            "title": "Урок от модератора",
            "description": "Описание урока от модератора",
            "video_link": "https://youtube.com/watch?v=mod123",
            "course": self.course.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)  # Урок не создан

    def test_lesson_update_by_moderator(self):
        """Тест обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.pk})
        data = {"title": "Урок обновлен модератором"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Урок обновлен модератором")

    def test_lesson_delete_by_moderator_forbidden(self):
        """Тест удаления урока модератором (должно быть запрещено)"""
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)  # Урок не удален

    def test_lesson_youtube_validator(self):
        """Тест валидатора YouTube ссылок"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lesson-list-create")

        # Валидная YouTube ссылка
        valid_data = {
            "title": "Урок с YouTube",
            "description": "Описание",
            "video_link": "https://youtube.com/watch?v=valid123",
            "course": self.course.id,
        }
        response = self.client.post(url, valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Невалидная ссылка
        invalid_data = {
            "title": "Урок с Vimeo",
            "description": "Описание",
            "video_link": "https://vimeo.com/123456789",
            "course": self.course.id,
        }
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("video_link", response.data)


class SubscriptionTestCase(APITestCase):
    """Тесты функционала подписок на курсы"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем пользователя
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            phone="+1234567890",
            city="Moscow",
        )

        # Создаем курс
        self.course = Course.objects.create(
            title="Тестовый курс для подписки",
            description="Описание курса",
            owner=self.user,
        )

    def test_subscription_create(self):
        """Тест создания подписки"""
        self.client.force_authenticate(user=self.user)
        url = reverse("course-subscription")
        data = {"course_id": self.course.id}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(response.data["subscribed"])
        self.assertEqual(Subscription.objects.count(), 1)

    def test_subscription_delete(self):
        """Тест удаления подписки"""
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        url = reverse("course-subscription")
        data = {"course_id": self.course.id}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(response.data["subscribed"])
        self.assertEqual(Subscription.objects.count(), 0)

    def test_subscription_toggle(self):
        """Тест переключения подписки"""
        self.client.force_authenticate(user=self.user)
        url = reverse("course-subscription")
        data = {"course_id": self.course.id}

        # Первый запрос - создание подписки
        response1 = self.client.post(url, data)
        self.assertEqual(response1.data["message"], "подписка добавлена")
        self.assertTrue(response1.data["subscribed"])

        # Второй запрос - удаление подписки
        response2 = self.client.post(url, data)
        self.assertEqual(response2.data["message"], "подписка удалена")
        self.assertFalse(response2.data["subscribed"])

    def test_subscription_without_course_id(self):
        """Тест подписки без указания ID курса"""
        self.client.force_authenticate(user=self.user)
        url = reverse("course-subscription")
        data = {}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_subscription_nonexistent_course(self):
        """Тест подписки на несуществующий курс"""
        self.client.force_authenticate(user=self.user)
        url = reverse("course-subscription")
        data = {"course_id": 99999}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscription_status_in_course_serializer(self):
        """Тест отображения статуса подписки в сериализаторе курса"""
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_subscribed"])

    def test_no_subscription_status_in_course_serializer(self):
        """Тест отсутствия подписки в сериализаторе курса"""
        self.client.force_authenticate(user=self.user)
        url = reverse("course-detail", kwargs={"pk": self.course.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_subscribed"])


class PaginationTestCase(APITestCase):
    """Тесты пагинации"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            phone="+1234567890",
            city="Moscow",
        )

        # Создаем много курсов для тестирования пагинации
        self.courses = []
        for i in range(15):
            course = Course.objects.create(
                title=f"Курс {i + 1}",
                description=f"Описание курса {i + 1}",
                owner=self.user,
            )
            self.courses.append(course)

        # Создаем много уроков
        self.lessons = []
        for i in range(25):
            lesson = Lesson.objects.create(
                title=f"Урок {i + 1}",
                description=f"Описание урока {i + 1}",
                video_link=f"https://youtube.com/watch?v=test{i + 1}",
                course=self.courses[i % len(self.courses)],
                owner=self.user,
            )
            self.lessons.append(lesson)

    def test_courses_pagination(self):
        """Тест пагинации курсов"""
        self.client.force_authenticate(user=self.user)
        url = reverse("course-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)  # page_size = 5
        self.assertEqual(response.data["count"], 15)
        self.assertIsNotNone(response.data["next"])

    def test_lessons_pagination(self):
        """Тест пагинации уроков"""
        self.client.force_authenticate(user=self.user)
        url = reverse("lesson-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)  # page_size = 10
        self.assertEqual(response.data["count"], 25)
        self.assertIsNotNone(response.data["next"])

    def test_custom_page_size(self):
        """Тест кастомного размера страницы"""
        self.client.force_authenticate(user=self.user)
        url = reverse("course-list")
        response = self.client.get(url, {"page_size": 3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_max_page_size_limit(self):
        """Тест ограничения максимального размера страницы"""
        self.client.force_authenticate(user=self.user)
        url = reverse("course-list")
        response = self.client.get(url, {"page_size": 100})  # Больше max_page_size = 20

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Должно вернуть не больше max_page_size
        self.assertLessEqual(len(response.data["results"]), 20)


class PermissionsTestCase(APITestCase):
    """Тесты системы прав доступа"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем группы
        self.moderators_group = Group.objects.create(name="Модераторы")

        # Создаем пользователей
        self.owner1 = User.objects.create_user(
            email="owner1@test.com",
            password="testpass123",
            first_name="Owner1",
            last_name="User",
            phone="+1234567890",
            city="Moscow",
        )

        self.owner2 = User.objects.create_user(
            email="owner2@test.com",
            password="testpass123",
            first_name="Owner2",
            last_name="User",
            phone="+1234567891",
            city="Moscow",
        )

        self.moderator = User.objects.create_user(
            email="moderator@test.com",
            password="testpass123",
            first_name="Moderator",
            last_name="User",
            phone="+1234567892",
            city="Moscow",
        )
        self.moderator.groups.add(self.moderators_group)

        # Создаем курсы разных владельцев
        self.course1 = Course.objects.create(
            title="Курс владельца 1", description="Описание", owner=self.owner1
        )

        self.course2 = Course.objects.create(
            title="Курс владельца 2", description="Описание", owner=self.owner2
        )

    def test_owner_sees_only_own_courses(self):
        """Тест: владелец видит только свои курсы"""
        self.client.force_authenticate(user=self.owner1)
        url = reverse("course-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Владелец 1 должен видеть только свой курс
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Курс владельца 1")

    def test_moderator_sees_all_courses(self):
        """Тест: модератор видит все курсы"""
        self.client.force_authenticate(user=self.moderator)
        url = reverse("course-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Модератор должен видеть все курсы
        self.assertEqual(response.data["count"], 2)

    def test_owner_cannot_edit_other_courses(self):
        """Тест: владелец не может редактировать чужие курсы"""
        self.client.force_authenticate(user=self.owner1)
        url = reverse("course-detail", kwargs={"pk": self.course2.pk})
        data = {"title": "Попытка редактирования"}

        response = self.client.patch(url, data)

        # Должна быть ошибка 404, так как курс не в queryset владельца 1
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
