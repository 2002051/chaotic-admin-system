# 自定制过滤器
from rest_framework.filters import BaseFilterBackend
from app01 import models

class BookFilterByKw(BaseFilterBackend):
    """图书搜索专用过滤器"""

    def filter_queryset(self, request, queryset, view):
        kw = request.query_params.get("kw","")
        if not kw:
            return queryset
        return queryset.filter(title__icontains=kw)

class CampusFilterByKw(BaseFilterBackend):
    """校区搜索专用过滤器"""

    def filter_queryset(self, request, queryset, view):
        kw = request.query_params.get("kw","")
        if not kw:
            return queryset
        return queryset.filter(title__icontains=kw)


class BiographicalFilterByKw(BaseFilterBackend):
    """简历列表专用过滤器"""
    def filter_queryset(self, request, queryset, view):
        kw = request.query_params.get("kw", "")
        if not kw:
            return queryset
        return queryset.filter(name__icontains=kw)

class StudentFilterByKw(BaseFilterBackend):
    """简历列表专用过滤器"""
    def filter_queryset(self, request, queryset, view):
        kw = request.query_params.get("kw", "")
        if not kw:
            return queryset
        return queryset.filter(nickname__icontains=kw)

class MediaFilterByKw(BaseFilterBackend):
    """媒体文件标题过滤器"""

    def filter_queryset(self, request, queryset, view):
        kw = request.query_params.get("kw", "")
        if not kw:
            return queryset
        return queryset.filter(title__icontains=kw)