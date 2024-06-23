from django import forms
import re
from app01 import models
from django_redis import get_redis_connection

class SmsForm(forms.Form):
    phone = forms.CharField()

    def clean_phone(self):
        pattern = re.compile(r'^1[3456789]\d{9}$')
        phone = self.data.get("phone")
        if not re.match(pattern, phone):
            raise Exception("手机号格式不正确")
        obj = models.User.objects.filter(phone=phone).first()
        if obj:
            raise Exception("手机号已存在")
        return self.data


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名")
    password = forms.CharField(label="密码")
    code = forms.CharField(label="图片验证码")
    def __init__(self, *args, **kwargs):
        self.ip = kwargs.pop('ip', None)
        super().__init__(*args, **kwargs)
    def clean_code(self):
        code = self.cleaned_data.get("code")
        ip = self.ip
        print(code,ip)
        conn = get_redis_connection("default")
        code_byte = conn.get(ip)

        if code != code_byte.decode():
            raise Exception("验证码错误！")
        return code
    def clean(self):
        print("self.cleaned_data1", self.cleaned_data)
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        code = self.cleaned_data.get("code")
        if not code:
            raise Exception("请输入验证码！")
        obj = models.User.objects.filter(username=username,password=password).first()
        if not obj:
            raise Exception("用户名或密码错误")
        return self.cleaned_data
