from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Кастомная пагинация на 5 элементов на странице.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100
