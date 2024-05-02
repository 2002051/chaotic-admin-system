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
from app01.views import admininfo, upload, book,campus,biographical,student
from api import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/register/", admininfo.RegisterView.as_view()),
    path("api/login/", admininfo.LoginView.as_view()),

    path("api/book/", book.BookView.as_view({"get": "list", "post": "create", "delete": "delete"})),
    path("api/book/<int:pk>/", book.BookView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    # path("api/book/search/",book.BookSearchView.as_view())，

    path("api/campus/", campus.CampusView.as_view({"get": "list", "post": "create", "delete": "delete"})),
    path("api/campus/<int:pk>/", campus.CampusView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),

    path("api/biographical/", biographical.BiographicalView.as_view({"get": "list", "post": "create", "delete": "delete"})),
    path("api/biographical/<int:pk>/", biographical.BiographicalView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),

    path("api/studentinfo/",student.StudentInfoView.as_view({"get": "list", "post": "create", "delete": "delete"})),
    path("api/studentinfo/<int:pk>/",student.StudentInfoView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),


    # 上传头像
    path("upload/", upload.AvatarUpload.as_view()),
    # 上传图书封面
    path("upload/bookimg/", upload.BookimgUpload.as_view()),
    # 上传pdf简历附件文件
    path("upload/biographical/",upload.BiographicalUpload.as_view()),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
