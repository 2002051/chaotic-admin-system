import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app01.utils.ser_ import RegisterSer, LoginSer
from app01 import models
from app01.utils.ser_ import BiographicalSer
from app01.utils.res_ import MyResponse
from app01.utils.auth_ import LoginAuth
from app01.utils.fil_ import BiographicalFilterByKw
from app01.utils.exc_ import MyException
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException, ValidationError



class BiographicalView(MyResponse,ModelViewSet):
    """简历(pdf)视图"""
    authentication_classes = [LoginAuth]
    queryset = models.Biographical.objects.all()
    serializer_class = BiographicalSer
    filter_backends = [BiographicalFilterByKw]


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
            models.Biographical.objects.filter(id__in=id_list).delete()  #
            return Response("删除成功")
        raise MyException("请求异常")
