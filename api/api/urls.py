"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from app01.views import admininfo, upload, book, campus, biographical, student, medias
from api import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/regist/", admininfo.RegistView.as_view()),
    path("api/register/", admininfo.RegisterView.as_view()),
    path("api/login/", admininfo.LoginView.as_view()),
    path("api/sms/", admininfo.SmsView.as_view()),
    path("api/codeimg/",admininfo.CodeImgView.as_view()),
    path("api/validate/token/",admininfo.ValidateTokenView.as_view()),
    # path("")

    path("api/book/", book.BookView.as_view({"get": "list", "post": "create", "delete": "delete"})),
    path("api/book/<int:pk>/", book.BookView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    # path("api/book/search/",book.BookSearchView.as_view())，

    path("api/campus/", campus.CampusView.as_view({"get": "list", "post": "create", "delete": "delete"})),
    path("api/campus/<int:pk>/", campus.CampusView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),

    path("api/biographical/",
         biographical.BiographicalView.as_view({"get": "list", "post": "create", "delete": "delete"})),
    path("api/biographical/<int:pk>/",
         biographical.BiographicalView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),

    path("api/student/", student.StudentInfoView.as_view({"get": "list", "post": "create", "delete": "delete"})),
    path("api/student/<int:pk>/",
         student.StudentInfoView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),

    path("api/medias/", medias.MediaView.as_view({"get": "list", "post": "create", "delete": "delete"})),
    path("api/medias/<int:pk>/", medias.MediaView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),

    # 视频播放相关
    path("api/video/list/", medias.VideoView.as_view()),
    path("api/video/blog/", medias.BlogView.as_view()),

    # 上传头像
    path("upload/", upload.AvatarUpload.as_view()),
    # 上传图书封面
    path("upload/bookimg/", upload.BookimgUpload.as_view()),
    # 上传pdf简历附件文件
    path("upload/biographical/", upload.BiographicalUpload.as_view()),
    # 上传学生照片
    path("upload/student/", upload.StudentUpload.as_view()),

    # 上传媒体图片
    path("upload/image/", upload.ImageUpload.as_view()),
    # 媒体音频
    path("upload/audio/", upload.AudioUpload.as_view()),
    # 媒体视频
    path("upload/video/", upload.VideoUpload.as_view()),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
