# 自定制过滤器
from rest_framework.filters import BaseFilterBackend
from app01 import models

class BookFilterByKw(BaseFilterBackend):
    """搜索专用过滤器"""

    def filter_queryset(self, request, queryset, view):
        kw = request.query_params.get("kw","")
        if not kw:
            return queryset
        return queryset.filter(title__icontains=kw)
