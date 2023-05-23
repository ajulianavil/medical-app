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
    path("registros/consulta/<int:param>", views.reporteInfo, name="registroinfo"),
    path("usuario/nuevo", views.agregar_usuario, name="usuario/nuevo"),
    path("registros", views.reportes, name="registros"),
    path("reporte_pdf/<int:idreporte_id>", views.reporte_pdf, name="reporte_pdf"),
    path("reporte/graficos/<int:idreporte_id>", views.reporte_graficos, name="reporte_graficos"),
    path('chart-data/<int:idreporte_id>/<str:nombreMedicion>/<str:ga>', views.chart_data_view, name='chart_data'),
    path("editPacientData/<int:consultaid>", views.editPacientData, name="editPacientData"),
    path("editReportData/<int:consultaid>", views.editReportData, name="editReportData"),
    path("usuario/listado", views.ver_usuarios, name="usuario/listado"),
    path("deactivateUser/<str:userid>", views.deactivateUser, name="deactivateUser"),
    path("reactivateUser/<str:userid>", views.reactivateUser, name="reactivateUser")
]