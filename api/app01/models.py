from django.db import models


# Create your models here.
class Admin(models.Model):
    """管理员"""
    nickname = models.CharField(verbose_name="昵称",max_length=64)
    avatar = models.CharField(verbose_name="头像",max_length=64,default="/media/avatar/default.jpg")
    username = models.CharField(verbose_name="用户名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)

class Book(models.Model):
    """图书"""
    title = models.CharField(verbose_name="图书标题",max_length=128)
    author = models.CharField(verbose_name="作者",max_length=128)
    image = models.CharField(verbose_name="封面图",max_length=128)
    price = models.IntegerField(verbose_name="价格(分)")


# class Detail(models.Model):
# """用户详情"""