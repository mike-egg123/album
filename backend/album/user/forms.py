# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from .models import Profile

# 扩展用户信息的表单
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)

