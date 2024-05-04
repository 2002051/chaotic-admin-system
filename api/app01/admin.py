from django.contrib import admin
from app01 import models
# Register your models here.


# admin.site.register(models.Campus)   # 可以使用另一种方式对模型类进行注册
@admin.register(models.Campus)
class DepartAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Admin)
# admin.site.register(models.Campus)
admin.site.register(models.Biographical)
admin.site.register(models.Book)
admin.site.register(models.Media)
admin.site.register(models.Stu)
admin.site.register(models.StudentInfo)
