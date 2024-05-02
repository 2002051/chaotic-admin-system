from django.db import models


# Create your models here.
class Admin(models.Model):
    """管理员"""
    nickname = models.CharField(verbose_name="昵称", max_length=64)
    avatar = models.CharField(verbose_name="头像", max_length=64, default="/media/avatar/default.jpg")
    username = models.CharField(verbose_name="用户名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)


class Book(models.Model):
    """图书"""
    title = models.CharField(verbose_name="图书标题", max_length=128)
    author = models.CharField(verbose_name="作者", max_length=128)
    image = models.CharField(verbose_name="封面图", max_length=128)
    price = models.IntegerField(verbose_name="价格(分)")


class Campus(models.Model):
    """校区"""
    title = models.CharField(verbose_name="校区名称", max_length=128)
    address = models.CharField(verbose_name="地址", max_length=128)
    detail = models.TextField(verbose_name="简介")
    # class Detail(models.Model):


# """用户详情"""

class StudentInfo(models.Model):
    nickname = models.CharField(verbose_name="昵称", max_length=64)
    avatar = models.CharField(verbose_name="照片", max_length=64, default="/media/userAvatar/default.jpg")
    campus = models.ForeignKey(verbose_name="校区",to="Campus",on_delete=models.CASCADE)
    birth = models.DateTimeField(verbose_name="出生日期")
    isgraduate = models.BooleanField(verbose_name="是否毕业",default=False)
    # createtime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)


class Biographical(models.Model):
    """简历"""
    name = models.CharField(verbose_name="姓名", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    choice_tul = (
        (1, "小学"), (2, "初中"), (3, "高中"), (4, "本科"), (5, "研究生"), (6, "博士"), (7, "其它"),
    )
    education = models.SmallIntegerField(verbose_name="教育水平", choices=choice_tul)
    attachment = models.CharField(verbose_name="简历附件", max_length=255)
