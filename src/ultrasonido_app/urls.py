from django.urls import path, include
from . import views

urlpatterns = [
    path("app", views.homepage, name="homepage"),
    path("consultas/nueva", views.agregar_consulta, name="consultas/nueva"),
    path("usuario/nuevo", views.agregar_usuario, name="usuario/nuevo"),
    path("registros", views.reportes, name="registros"),
    path("registros/consulta", views.reportes, name="registros"),
    path("registros/consulta/<int:param>", views.reporteInfo, name="registros"),
    
]