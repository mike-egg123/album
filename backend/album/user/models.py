from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    # 与User模型形成一对一的映射关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 头像
    avatar = models.ImageField(upload_to = "avatar/%Y%m%d/", blank = True)
