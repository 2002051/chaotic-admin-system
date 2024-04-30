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
from rest_framework.pagination import PageNumberPagination


class BookView(MyResponse, ModelViewSet):
    authentication_classes = [LoginAuth]
    serializer_class = BookSer
    queryset = models.Book.objects.all()
    """图书视图"""

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
