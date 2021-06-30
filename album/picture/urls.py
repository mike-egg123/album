from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello), # 打个招呼
    path('get_upload_token', views.get_upload_token), # 获得上传凭证
    path('get_download_token', views.get_download_token), # 获得下载凭证
    # path('get_modify_token', views.get_modify_token), # 考虑安全因素，拒绝发送管理token，由业务服务器完成操作
]