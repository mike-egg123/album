from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import json
import random
from django.shortcuts import render
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

def get_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        return JsonResponse({
            "token": tools.get_token(name)
        })
    else:
        return JsonResponse({
            "message": "error method!"
        })