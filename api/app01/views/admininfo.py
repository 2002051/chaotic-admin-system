# 管理员相关
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from app01.utils.ser_ import RegisterSer, LoginSer, RegistSer
from app01 import models
from app01.utils.res_ import MyResponse


class RegistView(MyResponse, APIView):
    """移动端需要短信验证码的注册"""

    def post(self, request):
        ser = RegistSer(data=request.data)
        ser.is_valid(raise_exception=True)
        code = ser.validated_data.pop("code")
        # print("666")
        obj = models.User.objects.create(**ser.validated_data)
        return Response("注册成功")


class RegisterView(MyResponse, APIView):
    """注册"""

    def post(self, request):
        ser = RegisterSer(data=self.request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response("ok")


from app01.utils.form_ import LoginForm
from app01.utils.jwt_ import get_jwt


class LoginView(MyResponse, APIView):
    """登录"""

    def post(self, request):
        form = LoginForm(data=request.data,ip=request.META['REMOTE_ADDR'])
        print(123)
        isT = form.is_valid()

        # print("isT",isT)
        token = get_jwt({**form.cleaned_data})
        print("token",token)
        return Response(token)


    # def post(self, request):
    #     ser = LoginSer(data=request.data)
    #     ser.is_valid(raise_exception=True)
    #     token = ser.validated_data.pop("token")
    #     obj = models.Admin.objects.filter(**ser.validated_data).first()
    #     ser_2 = LoginSer(instance=obj)
    #     return Response({"data": ser_2.data, "token": token})


from app01.utils.form_ import SmsForm
from django_redis import get_redis_connection
import random


class SmsView(MyResponse, APIView):
    def post(self, request):
        form = SmsForm(data=request.data)
        if form.is_valid():
            phone = request.data.get("phone")
            code = random.randint(1000, 9999)
            conn = get_redis_connection("default")
            conn.set(phone, code, ex=60)
            print("code:", code)
            return Response("发送成功")
        raise Exception("失败")


from app01.utils.imgcode import check_code

import base64
import io


class CodeImgView(MyResponse, APIView):
    def get(self, request):
        img, code = check_code()
        # 将图像转换为字节流
        byte_io = io.BytesIO()
        img.save(byte_io, format="PNG")
        byte_io.seek(0)
        # 获取base64编码的字符串
        base64_str = base64.b64encode(byte_io.getvalue()).decode('utf-8')
        ip = request.META['REMOTE_ADDR']
        conn = get_redis_connection("default")
        conn.set(ip, code)
        print(ip, code)
        # print(img, code, base64_str)
        return Response(base64_str)
