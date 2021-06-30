from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile, User
from .forms import ProfileForm
import json
import random


# 打招呼
def hello(request):
    if request.method == 'POST':
        return JsonResponse({
            "message": "hello guy!"
        })
    else:
        return JsonResponse({
            "message": "error method!"
        })

# 登录并获取个人信息
def my_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username is not None and password is not None:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if Profile.objects.filter(user=user).exists():
                    userprofile = Profile.objects.get(user=user)
                else:
                    userprofile = Profile.objects.create(user=user)
                if userprofile.avatar and hasattr(userprofile.avatar, 'url'):
                    avatar = "http://182.92.239.145" + str(userprofile.avatar.url)
                else:
                    avatar = ""
                return JsonResponse({
                    "status": 0,
                    "userid": user.id,
                    "username": username,
                    "email": user.email,
                    "avatar": avatar
                })
            else:
                return JsonResponse({
                    "status": 1
                })
        else:
            return JsonResponse({
                "status": 2
            })
    else:
        return JsonResponse({
            "status": 100
        })

# 注册
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        if username is not None and password is not None and email is not None:
            # 保证email的唯一性
            users = User.objects.filter(email=email)
            if len(users) > 0:
                return JsonResponse({
                    "status":1
                })
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                login_user = authenticate(request, username=username, password=password)
                if login_user:
                    login(request, login_user)
                    return JsonResponse({
                        "status": 0,
                        "userid": user.id,
                        "user":{
                            "username":username,
                            "email":email,
                            "avatar":""
                        }
                    })
            except:
                return JsonResponse({
                    "status": 1
                })
        else:
            return JsonResponse({
                "status": 2
            })
    else:
        return JsonResponse({
            "status": 100
        })

# 注销
def my_logout(request):
    logout(request)
    return JsonResponse({
        "status": 0
    })

# 完善个人信息
def change_personality(request):
    if request.method == 'POST':
        user = request.user
        # 尚未登录，无法完善个人信息
        if user.id == None:
            return JsonResponse({
                "status":2
            })
        profile = Profile.objects.get(user=user)
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            if 'avatar' in request.FILES:
                avatar = profile_cd['avatar']
            else:
                avatar = profile.avatar
            profile.avatar = avatar
            profile.save()
            return JsonResponse({
                "status": 0
            })
        else:
            return JsonResponse({
                "status": 1
            })
    else:
        return JsonResponse({
            "status": 100
        })

# 生成验证码
def range_num(num):
    # 定义一个种子，从这里面随机拿出一个值，可以是字母
    seeds = "1234567890"
    # 定义一个空列表，每次循环，将拿到的值，加入列表
    random_num = []
    # choice函数：每次从seeds拿一个值，加入列表
    for i in range(num):
        random_num.append(random.choice(seeds))
    # 将列表里的值，变成四位字符串
    return "" . join(random_num)#5454

# 发送邮件
def send_msg(email, valid_code):
    send_mail('找回密码', "验证码为：" + valid_code, settings.DEFAULT_FROM_EMAIL,
              [email], fail_silently=False)
    return

# 获取验证码并验证
def valid(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        type = data.get('type')
        if type == 'send':
            valid_code = range_num(6)
            keyword = data.get('keyword')
            if "@" not in keyword:
                user = User.objects.filter(username=keyword)
                if len(user) == 0:
                    return JsonResponse({
                        'status':1
                    })
                keyword = user[0].email
            else:
                user = User.objects.filter(email=keyword)
                if len(user) == 0:
                    return JsonResponse({
                        'status': 1
                    })
            send_msg(keyword, valid_code)
            return JsonResponse({
                'status':0,
                "valid_code":valid_code
            })
    else:
        return JsonResponse({
            'status':100
        })

# 修改密码
def change_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        keyword = data.get('keyword')
        try:
            if "@" in keyword:
                user = User.objects.get(email=keyword)
            else:
                user = User.objects.get(username=keyword)
        except:
            return JsonResponse({
                'status':1
            })
        password = data.get('password')
        user.set_password(password)
        user.save()
        return JsonResponse({
            'status':0
        })
    else:
        return JsonResponse({
            'status':100
        })

