import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app01.utils.ser_ import RegisterSer, LoginSer
from app01 import models
from app01.utils.ser_ import CampusSer
from app01.utils.res_ import MyResponse
from app01.utils.auth_ import LoginAuth
from app01.utils.fil_ import CampusFilterByKw
from app01.utils.exc_ import MyException
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException, ValidationError
from django.utils.translation import gettext_lazy as _



class CampusView(MyResponse,ModelViewSet):
    authentication_classes = [LoginAuth]
    serializer_class = CampusSer
    queryset = models.Campus.objects.all()
    filter_backends = [CampusFilterByKw]

    def destroy(self, request, *args, **kwargs):
        # 修改一下delete请求的状态码，否则前端拿不到请求数据
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        """批量删除"""
        id_list = request.data.get("id_list", "")
        id_list = json.loads(id_list)
        if id_list:
            models.Campus.objects.filter(id__in=id_list).delete()  #
            return Response("删除成功")
        raise MyException("请求异常")
