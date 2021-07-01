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
from fuzzywuzzy import fuzz

# Create your views here.

FUZZY_INDEX = 40


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
            pic = Picture(name=name, pformat=name.split(".")[-1])
            pic.user = user
            pic.save()
            pic.node = datetime.datetime.strftime(pic.create_date, '%Y%m%d') + "_" + pic.pk + "." + pic.pformat
            pic.save()
            return JsonResponse({
                "status": 0,
                "node": pic.node,
                "pid": pic.pk
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
            if (pic is None):
                return JsonResponse({
                    "status": 3,
                })
            else:
                pic.is_upload = 1
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


def delete_pic(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            pid = data.get("pid")
            pic = Picture.objects.filter(pk=pid).first()
            if (pic is None):
                return JsonResponse({
                    "status": 3,
                })
            else:
                tools.delete_pic(pic.node)
                pic.delete()
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


def rename_pic(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            pid = data.get("pid")
            name = data.get("name")
            pic = Picture.objects.filter(pk=pid).first()
            if (pic is None):
                return JsonResponse({
                    "status": 3,
                })
            else:
                pic.name = name
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


def search_pic(request):
    '''
    1: category //五类中的一类
    2: description //nlp生成的描述
    3: date //查询格式：yyyymmdd。例如：20210701
    4: name
    5: pid
    6: tag //直接返回的一堆tag
    7: format
    8: node
    9: description 模糊
    10: all
    '''

    '''
            if type==0:
            courses = Course.objects.all()
            for course in courses:
                num = fuzz.token_sort_ratio(value, course.name)
                if num>40:
                    result.append(get_simple_info(course))
    '''

    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            uid = data.get("uid")
            type = data.get("type")
            msg = data.get("msg")
            # pics = Picture.objects.filter()
            result = []
            if type == 1:
                pics = Picture.objects.filter(user__pk=uid, category__name__iexact=msg)
            elif type==2:
                pics = Picture.objects.filter(user__pk=uid, description__icontains=msg)
            elif type==3:
                pics = Picture.objects.filter(user__pk=uid, node__istartswith=msg)
            elif type==4:
                pics = Picture.objects.filter(user__pk=uid, name__icontains=msg)
            elif type==5:
                pics = Picture.objects.filter(user__pk=uid, pk=int(msg))
            elif type==6:
                pics = Picture.objects.filter(user__pk=uid, tag__icontains=msg)
            elif type==7:
                pics = Picture.objects.filter(user__pk=uid, pformat__exact=msg)
            elif type==8:
                pics = Picture.objects.filter(user__pk=uid, node__exact=msg)
            elif type==9:
                mpics = Picture.objects.filter(user__pk=uid)
                pics = []
                for pic in mpics:
                    if fuzz.ratio(msg, pic.description) > FUZZY_INDEX:
                        pics.append(pic)
            elif type==10:
                pics = Picture.objects.filter(user__pk=uid)
            else:
                return JsonResponse({
                    "status": 1
                })
            for pic in pics:
                result.append(tools.get_full_info(pic))

            return JsonResponse({
                "status": 0,
                "total": len(result),
                "result": result
            })

        except:
            return JsonResponse({
                "status": 1
            })
    else:
        return JsonResponse({
            "status": 2
        })
