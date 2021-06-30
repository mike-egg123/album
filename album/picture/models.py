from django.db import models
from ..user.models import User

# Create your models here.
from django.db import models

# Create your models here.


class Category(models.Model):
    # 名称
    name = models.CharField(max_length=300)
    # # 代表
    # representation = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name="pictures")

class Picture(models.Model):
    # 名称
    name = models.CharField(max_length=300)
    # 所有者
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pictures")
    # 创建日期
    create_date = models.DateTimeField(auto_now_add=True)
    # 修改日期
    modify_date = models.DateTimeField(auto_now=True)
    # 类别
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="pictures")

