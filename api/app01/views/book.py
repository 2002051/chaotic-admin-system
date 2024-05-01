import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app01.utils.ser_ import RegisterSer, LoginSer
from app01 import models
from app01.utils.ser_ import BookSer
from app01.utils.res_ import MyResponse
from app01.utils.auth_ import LoginAuth
from app01.utils.fil_ import BookFilterByKw
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException, ValidationError
from django.utils.translation import gettext_lazy as _


class BookException(APIException):
    status = status.HTTP_200_OK
    default_detail = _('请求异常')
    default_code = 'error'


class BookView(MyResponse, ModelViewSet):
    """图书视图"""

    authentication_classes = [LoginAuth]
    serializer_class = BookSer
    queryset = models.Book.objects.all().order_by("id")
    filter_backends = [BookFilterByKw]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        """批量删除"""
        id_list = request.data.get("id_list", "")
        id_list = json.loads(id_list)
        if id_list:
            models.Book.objects.filter(id__in=id_list).delete()
            return Response("删除成功")
        raise BookException("请求异常")

