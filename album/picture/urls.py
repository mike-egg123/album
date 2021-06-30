from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello), # 打个招呼
    path('get_token', views.get_token), # 获得上传凭证
]