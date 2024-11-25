from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.conf import settings

class CustomLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'per_page' 
    offset_query_param = 'start_from' 
    
    default_limit = getattr(settings, 'PAGE_SIZE', 10)  
    max_limit = getattr(settings, 'MAX_PAGE_SIZE', 50)

    def get_paginated_response(self, data):
        current_page = (self.offset // self.limit) + 1
        total_pages = (self.count // self.limit) + (1 if self.count % self.limit > 0 else 0)
        return Response({
            "pagination": {
                "total_count": self.count,
                "total_pages": total_pages,
                "current_page": current_page,
                "per_page": self.limit,
                "next_page": self.get_next_link(),
                "previous_page": self.get_previous_link()
            },
            "results": data
        })
