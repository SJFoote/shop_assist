from django.urls import path     
from . import views

urlpatterns = [
    # renders
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('checkout/', views.checkOut),

    # redirects

]