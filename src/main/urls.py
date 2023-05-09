from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("consultas/nueva", views.agregar_consulta, name="consultas/nueva"),
    path("landing", views.landing, name="landing"),
    path("aboutUs", views.aboutUs, name="aboutUs"),
    path("howToRegister", views.howToRegister, name="howToRegister"),
    path("repositorio", views.repositorio, name="repositorio") ,
     
]