# 序列化器
import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app01 import models
from app01.utils.jwt_ import get_jwt


class RegisterSer(serializers.ModelSerializer):
    class Meta:
        model = models.Admin
        fields = "__all__"

    def validate_username(self, value):
        admininfo = models.Admin.objects.filter(username=value).first()
        print("admininfo", admininfo)
        if admininfo:
            # 管理员不存在
            raise ValidationError("该用户名已被人使用")
        return value


class LoginSer(serializers.ModelSerializer):
    nickname = serializers.CharField(read_only=True)
    avatar = serializers.CharField(read_only=True)

    class Meta:
        model = models.Admin
        fields = "__all__"

    def validate(self, attrs):
        obj = models.Admin.objects.filter(**attrs).first()
        if not obj:
            raise ValidationError({"err": "用户名或者密码错误"})
        # 校验通过生成jtw
        payload = {
            **attrs,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60 * 24 * 7)  # 超时时间一个礼拜
        }
        attrs["token"] = get_jwt(payload=payload)
        return attrs


class BookSer(serializers.ModelSerializer):
    """图书视图序列化器"""
    class Meta:
        model = models.Book
        fields = "__all__"
