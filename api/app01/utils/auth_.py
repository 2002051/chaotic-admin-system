# 认证组件

# 认证，部分请求没有登录是无法发送成功的..
from rest_framework.authentication import BaseAuthentication
import jwt
from django.conf import settings
from app01 import models
from rest_framework.exceptions import AuthenticationFailed


class LoginAuth(BaseAuthentication):
    """登录状态认证（可根据请求判断是否执行）"""

    def authenticate(self, request):
        # 如果是预检则跳过认证
        if request.method=="OPTIONS":
            return
        try:
            token = request.headers.get("token")
            # 解开token 从获取用户名密码，然后校验
            userinfo = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            username = userinfo.get("username")
            password = userinfo.get("password")
            print(username, password)
            userobj = models.Admin.objects.filter(username=username, password=password).first()
            if userobj:
                return userobj, token  # request.user  request.auth
            raise AuthenticationFailed("认证失败,请重新登录")
        except:
            raise AuthenticationFailed("认证失败")

    def authenticate_header(self, request):
        return "API"


class LoginAuth2(BaseAuthentication):
    """登录状态认证（可根据请求判断是否执行）"""

    def __init__(self, user_methods):
        self.user_methods = user_methods

    def authenticate(self, request):
        if request.method == "OPTIONS":
            # 预检不进行权限校验。
            return
        if request.method in self.user_methods:
            # 请求方法与self.user_methods一致的话则不需要执行对应的认证内容。
            return
        try:
            token = request.headers.get("token")
            # 解开token 从获取用户名密码，然后校验
            userinfo = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            username = userinfo.get("username")
            password = userinfo.get("password")
            print(password, username)
            userobj = models.Admin.objects.filter(username=username, password=password).first()

            if userobj:
                return userobj, token  # request.user  request.auth
            raise AuthenticationFailed("认证失败,劝你重新登录")
        except:
            raise AuthenticationFailed("后台异常，请联系开发者ytw")

    def authenticate_header(self, request):
        return "API"
