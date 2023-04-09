from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("consultas/nueva", views.agregar_consulta, name="consultas/nueva")
]