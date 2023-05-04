from django.urls import path, include
from . import views

urlpatterns = [
    path("landing", views.landing, name="landing"),
    path("aboutUs", views.aboutUs, name="aboutUs"),
    path("howToRegister", views.howToRegister, name="howToRegister")    
]