from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("consultas/nueva", views.agregar_consulta, name="consultas/nueva"),
    path("landing", views.landing, name="landing"),
    path("aboutUs", views.aboutUs, name="aboutUs"),
    path("howToRegister", views.howToRegister, name="howToRegister"),
    path("repositorio", views.repositorio, name="repositorio") ,
    path("historia_clinica", views.historia_clinica, name="historia_clinica")    ,
    path("registros/consulta", views.reportes, name="registros"),
    path("registros/consulta/<int:param>", views.reporteInfo, name="registros"),
    path("usuario/nuevo", views.agregar_usuario, name="usuario/nuevo"),
    path("registros", views.reportes, name="registros"),
    path("reporte_pdf/<int:idreporte_id>", views.reporte_pdf, name="reporte_pdf")
     
]