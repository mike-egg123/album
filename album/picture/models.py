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
    # 图片编号，唯一存在，用来确定图片资源，=create_time+'_'+id
    node = models.CharField(max_length=300, unique=True, default=None)
    # 创建日期
    create_date = models.DateTimeField(auto_now_add=True)
    # 修改日期
    modify_date = models.DateTimeField(auto_now=True)
    # 类别
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="pictures", null=True)
    # 所有标签
    tag = models.CharField(max_length=300, null=True)
    # 描述，使用nlp生成
    description = models.CharField(max_length=300, null=True)
    # 图片是否上传成功，成功为1
    is_upload = models.IntegerField(default=0)
    # 图片格式
    pformat = models.CharField(max_length=300)

