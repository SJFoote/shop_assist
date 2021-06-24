from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'loginReg.html')

def register(request):
    return render(request, 'loginReg.html')

def checkOut(request):
    return render(request, 'checkout.html')