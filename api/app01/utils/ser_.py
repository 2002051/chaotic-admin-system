# 序列化器
import datetime
import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app01 import models
from app01.utils.jwt_ import get_jwt

class RegistSer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate_username(self,value):
        print("value",value)
        obj = models.User.objects.filter(username=value).first()
        if obj:
            raise Exception("用户名已存在")
        return value
    # def validate_phone(self, value):
    #     obj = models.User.objects.filter(phone=value).first()
        # pattern = re.compile(r'^1[3456789]\d{9}$')
        # phone = self.initial_data.get("phone")
        # if not re.match(pattern, phone):
        #     raise Exception("手机号格式不正确")


    def validate_code(self, value):
        conn = get_redis_connection("default")
        phone = self.initial_data.get("phone")
        # print("aaa")
        try:
            code = conn.get(phone).decode()
        except:
            raise Exception("验证码未发送或已过期")
        if(code!=value):
            raise Exception("验证码错误")
        return value
    # def validate(self, attrs):
    #     print("attrs",attrs)
    #     # raise Exception("sv")
    #     return attrs


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


class CampusSer(serializers.ModelSerializer):
    """校区序列化器"""

    class Meta:
        model = models.Campus
        fields = "__all__"


class BiographicalSer(serializers.ModelSerializer):
    """pdf简历序列化器"""
    education = serializers.IntegerField(write_only=True)
    education_dict = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Biographical
        fields = "__all__"

    def get_education_dict(self, obj):
        return {
            "k": obj.education,
            "v": obj.get_education_display()
        }


class StudentInfoSer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentInfo
        fields = "__all__"
        # depth = 1


class MediaSer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = "__all__"

class VideoSer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    video = serializers.CharField()
