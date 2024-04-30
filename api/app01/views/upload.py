import os
import random

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from app01.utils.auth_ import LoginAuth
from app01.utils.res_ import MyResponse

class FileUploadException(APIException):
    """文件上传异常"""
    status_code = status.HTTP_200_OK

class AvatarUpload(MyResponse, APIView):
    # authentication_classes = [LoginAuth]
    """注册页上传头像"""
    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        if file_obj is None:
            return Response({'error': '上传失败'}, status=status.HTTP_400_BAD_REQUEST)
        file_name = str(random.randint(1000000,9999999)) + file_obj.name
        to_save_path = settings.MEDIA_URL + "avator" + "/" + file_name
        file_path = os.path.join(settings.MEDIA_ROOT, "avatar", file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        return Response({'message': '上传成功', "path": to_save_path}, status=status.HTTP_200_OK)


class BookimgUpload(MyResponse,APIView):
    """上传图书图片"""

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        if file_obj is None:
            return Response({'error': '上传失败'}, status=status.HTTP_400_BAD_REQUEST)
        file_name = str(random.randint(1000000, 9999999)) + file_obj.name
        to_save_path = settings.MEDIA_URL + "book_img" + "/" + file_name
        file_path = os.path.join(settings.MEDIA_ROOT, "book_img", file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        return Response({'message': '上传成功', "path": to_save_path}, status=status.HTTP_200_OK)
