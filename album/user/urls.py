from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello), # 打个招呼
    path('login', views.my_login),  # 登录并获取个人信息
    path('register', views.register),  # 注册
    path('logout', views.my_logout), # 注销
    path('personality', views.change_personality), # 完善个人信息
    path('valid', views.valid), # 获取邮箱验证码并验证
    path('change_password', views.change_password), # 修改密码


]