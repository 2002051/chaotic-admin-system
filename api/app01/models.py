from django.db import models

class User(models.Model):
    """移动端用户"""
    username = models.CharField(verbose_name="用户名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)
    phone = models.CharField(verbose_name="手机号", max_length=11)



# Create your models here.
class Admin(models.Model):
    """管理员"""
    nickname = models.CharField(verbose_name="昵称", max_length=64)
    avatar = models.CharField(verbose_name="头像", max_length=64, default="/media/avatar/default.jpg")
    username = models.CharField(verbose_name="用户名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)
    class Meta:
        verbose_name = "管理员"
        verbose_name_plural = "管理员"  # 复数形式
    def __str__(self):
        return self.nickname

class Book(models.Model):
    """图书"""
    title = models.CharField(verbose_name="图书标题", max_length=128)
    author = models.CharField(verbose_name="作者", max_length=128)
    image = models.CharField(verbose_name="封面图", max_length=128)
    price = models.IntegerField(verbose_name="价格(分)")
    class Meta:
        verbose_name = "图书"
        verbose_name_plural = "图书"  # 复数形式
    def __str__(self):
        return self.title

class Campus(models.Model):
    """校区"""
    title = models.CharField(verbose_name="校区名称", max_length=128)
    address = models.CharField(verbose_name="地址", max_length=128)
    detail = models.TextField(verbose_name="简介")
    # class Detail(models.Model):
    class Meta:
        verbose_name = "校区"
        verbose_name_plural = "校区"  # 复数形式
    def __str__(self):
        return self.title

# """用户详情"""

class StudentInfo(models.Model):
    nickname = models.CharField(verbose_name="昵称", max_length=64)
    avatar = models.CharField(verbose_name="照片", max_length=64, default="/media/userAvatar/default.jpg")
    campus = models.ForeignKey(verbose_name="校区", to="Campus", on_delete=models.CASCADE)
    birth = models.DateTimeField(verbose_name="出生日期")
    isgraduate = models.BooleanField(verbose_name="是否毕业", default=False)
    # createtime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    class Meta:
        verbose_name = "学生"
        verbose_name_plural = "学生"  # 复数形式
    def __str__(self):
        return self.nickname

class Biographical(models.Model):
    """简历"""
    name = models.CharField(verbose_name="姓名", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    choice_tul = (
        (1, "小学"), (2, "初中"), (3, "高中"), (4, "本科"), (5, "研究生"), (6, "博士"), (7, "其它"),
    )
    education = models.SmallIntegerField(verbose_name="教育水平", choices=choice_tul)
    attachment = models.CharField(verbose_name="简历附件", max_length=255)
    class Meta:
        verbose_name = "简历"
        verbose_name_plural = "简历"  # 复数形式
    def __str__(self):
        return self.name

class Media(models.Model):
    """媒体展示表"""
    title = models.CharField(verbose_name="标题", max_length=64)
    image = models.CharField(verbose_name="图片", max_length=128)
    audio = models.CharField(verbose_name="音频", max_length=128)
    video = models.CharField(verbose_name="视频", max_length=128)
    create_time = models.DateTimeField(verbose_name="上传时间",auto_now_add=True)

    class Meta:
        verbose_name = "媒体"
        verbose_name_plural = "媒体"  # 复数形式
    def __str__(self):
        return self.title

class Stu(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    def __str__(self):
        return self.name