from rest_framework.pagination import PageNumberPagination


class CoursesPagination(PageNumberPagination):
    """Пагинатор для курсов"""
    page_size = 5  # Количество курсов на странице по умолчанию
    page_size_query_param = 'page_size'  # Параметр для изменения размера страницы
    max_page_size = 20  # Максимальное количество элементов на странице


class LessonsPagination(PageNumberPagination):
    """Пагинатор для уроков"""
    page_size = 10  # Количество уроков на странице по умолчанию
    page_size_query_param = 'page_size'  # Параметр для изменения размера страницы
    max_page_size = 50  # Максимальное количество элементов на странице


class StandardResultsSetPagination(PageNumberPagination):
    """Стандартный пагинатор для общего использования"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
