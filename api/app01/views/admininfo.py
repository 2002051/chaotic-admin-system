# 管理员相关
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from app01.utils.ser_ import RegisterSer, LoginSer
from app01 import models
from app01.utils.res_ import MyResponse


class RegisterView(MyResponse,APIView):
    """注册"""

    def post(self, request):
        ser = RegisterSer(data=self.request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response("ok")


class LoginView(MyResponse,APIView):
    """登录"""

    def post(self, request):
        ser = LoginSer(data=request.data)
        ser.is_valid(raise_exception=True)
        token = ser.validated_data.pop("token")
        obj = models.Admin.objects.filter(**ser.validated_data).first()
        ser_2 = LoginSer(instance=obj)
        return Response({"data": ser_2.data, "token": token})
