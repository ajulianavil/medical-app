from django.urls import path, include
from . import views

urlpatterns = [
    path("app", views.homepage, name="homepage"),
    path("consultas/nueva", views.agregar_consulta, name="consultas/nueva"),
    path("usuario/nuevo", views.agregar_usuario, name="usuario/nuevo"),
    
]