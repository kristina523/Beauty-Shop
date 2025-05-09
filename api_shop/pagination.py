from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class NumberedPagePagination(PageNumberPagination):
    page_size = 5  # или любое другое число

    def get_paginated_response(self, data):
        total_pages = self.page.paginator.num_pages
        current = self.page.number
        page_numbers = list(range(1, total_pages + 1))
        return Response({
            'count': self.page.paginator.count,
            'total_pages': total_pages,
            'current_page': current,
            'page_numbers': page_numbers,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })