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
        # file_name = str(random.randint(1000000, 9999999)) + file_obj.name
        # to_save_path = settings.MEDIA_URL + "avator" + "/" + file_name
        # file_path = os.path.join(settings.MEDIA_ROOT, "avatar", file_name)
        #
        # with open(file_path, 'wb+') as destination:
        #     for chunk in file_obj.chunks():
        #         destination.write(chunk)
        #
        # return Response({'message': '上传成功', "path": to_save_path}, status=status.HTTP_200_OK)
        file_name = file_obj.name
        file_path = os.path.join(settings.MEDIA_ROOT, "avatar", file_name)

        count = 1
        while os.path.exists(file_path):
            file_name = f"{os.path.splitext(file_obj.name)[0]} ({count}){os.path.splitext(file_obj.name)[1]}"
            file_path = os.path.join(settings.MEDIA_ROOT, "avatar", file_name)
            count += 1


        # to_save_path = os.path.join(settings.MEDIA_URL, "biographical", file_name)
        to_save_path = settings.MEDIA_URL + "avatar" + "/" + file_name
        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        return Response({'success': '上传成功', 'path': to_save_path}, status=status.HTTP_200_OK)

class BookimgUpload(MyResponse, APIView):
    """上传图书图片"""

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        if file_obj is None:
            return Response({'error': '上传失败'}, status=status.HTTP_400_BAD_REQUEST)
        # file_name = str(random.randint(1000000, 9999999)) + file_obj.name
        # to_save_path = settings.MEDIA_URL + "book_img" + "/" + file_name
        # file_path = os.path.join(settings.MEDIA_ROOT, "book_img", file_name)
        # with open(file_path, 'wb+') as destination:
        #     for chunk in file_obj.chunks():
        #         destination.write(chunk)
        # return Response({'message': '上传成功', "path": to_save_path}, status=status.HTTP_200_OK)
        # 获取文件名
        file_name = file_obj.name
        file_path = os.path.join(settings.MEDIA_ROOT, "book_img", file_name)


        count = 1
        while os.path.exists(file_path):

            file_name = f"{os.path.splitext(file_obj.name)[0]} ({count}){os.path.splitext(file_obj.name)[1]}"
            file_path = os.path.join(settings.MEDIA_ROOT, "book_img", file_name)
            count += 1

        to_save_path = settings.MEDIA_URL + "book_img" + "/" + file_name

        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        return Response({'success': '上传成功', 'path': to_save_path}, status=status.HTTP_200_OK)


class BiographicalUpload(MyResponse, APIView):
    '''简历附件上传'''

    def post(self, request):
        file_obj = request.FILES.get('file', "")

        if file_obj is None:
            return Response({'error': '上传失败'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取文件名
        file_name = file_obj.name
        file_path = os.path.join(settings.MEDIA_ROOT, "biographical", file_name)

        # 判断文件是否已存在
        count = 1
        while os.path.exists(file_path):
            # 文件名后添加编号
            file_name = f"{os.path.splitext(file_obj.name)[0]} ({count}){os.path.splitext(file_obj.name)[1]}"
            file_path = os.path.join(settings.MEDIA_ROOT, "biographical", file_name)
            count += 1

        to_save_path = settings.MEDIA_URL + "biographical" + "/" + file_name

        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        return Response({'success': '上传成功', 'path': to_save_path}, status=status.HTTP_200_OK)
