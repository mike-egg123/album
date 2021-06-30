from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import json
import random
from django.shortcuts import render
from models import Picture, Category
from ..user.models import User
import datetime
import tools

# Create your views here.

def hello(request):
    if request.method == 'POST':
        return JsonResponse({
            "message": "hello guy!"
        })
    else:
        return JsonResponse({
            "message": "error method!"
        })

def get_upload_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('node')
        policy = data.get('policy')
        return JsonResponse({
            "token": tools.upload_token(name, policy)
        })
    else:
        return JsonResponse({
            "message": "error method!"
        })

def get_download_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('node')
        # policy = data.get('policy')
        return JsonResponse({
            # "token": tools.download_token(name, policy)
            "url": tools.download_token(name)
        })
    else:
        return JsonResponse({
            "message": "error method!"
        })

# def get_modify_token(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         name = data.get('name')
#         policy = data.get('policy')
#         return JsonResponse({
#             "token": tools.modify_token(name, policy)
#         })
#     else:
#         return JsonResponse({
#             "message": "error method!"
#         })

def add_pic(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            name = data.get('name', default="未命名")
            uid = data.get('uid')
            user = User.objects.filter(pk=uid).first()
            pic = Picture(name=name)
            pic.user = user
            pic.save()
            pic.node = datetime.datetime.strftime(pic.create_date, '%Y%m%d')+"_"+pic.pk
            pic.save()
            return JsonResponse({
                "status": 0,
                "node": pic.node
            })
        except:
            return JsonResponse({
                "status": 1
            })
    else:
        return JsonResponse({
            "status": 2
        })

def confirm_pic(request):
    if request.method == 'POST':
        # data = json.loads(request.body)
        try:
            pid = request.POST.get("pid")
            pic = Picture.objects.filter(pk=pid).first()
            if(pic is None):
                return JsonResponse({
                    "status": 3,
                })
            else:
                pic.is_upload = 1
                pic.save()
                return JsonResponse({
                    "status": 0,
                })
        except:
            return JsonResponse({
                "status": 1
            })
    else:
        return JsonResponse({
            "status": 2
        })


