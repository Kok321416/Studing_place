from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Общий пагинатор для всех эндпоинтов проекта.
    Унифицированный класс пагинации с настраиваемыми параметрами.
    """
    page_size = 5  # Количество элементов на странице по умолчанию
    page_size_query_param = 'page_size'  # Параметр для изменения размера страницы
    max_page_size = 50  # Максимальное количество элементов на странице


# Алиасы для обратной совместимости
CoursesPagination = StandardResultsSetPagination
LessonsPagination = StandardResultsSetPagination
