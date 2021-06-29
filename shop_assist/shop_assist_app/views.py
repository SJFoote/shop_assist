from django.shortcuts import render, redirect, HttpResponse
from . import rainForest
from .models import *

# Create your views here.
def index(request):
    
    context = {    
    "bookList" : Book.objects.getTitles(),
    }
    return render(request, 'index.html', context)

def login(request):
    return render(request, 'loginReg.html')

def register(request):
    return render(request, 'loginReg.html')

def checkOut(request):
    return render(request, 'checkout.html')