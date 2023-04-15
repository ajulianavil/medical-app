from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("registro", views.register, name="register"),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('registro2', views.contact, name='registro2'),
]