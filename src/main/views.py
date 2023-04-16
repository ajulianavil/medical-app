from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from .models import *
from .serializers import *
from main.forms import UploadFileForm
from .data_processing import process_data
from rest_framework.decorators import api_view
from .Exceptions.PersonalizedExceptions import MyCustomException

# Create your views here.
def landing(request):
    return render(request, 'main/pages/landing.html')

def aboutUs(request):
    return render(request, 'main/pages/aboutUs.html')

def howToRegister(request):
    return render(request, 'main/pages/howToRegister.html' )
def homepage(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    current_user = request.user
    user = get_user_model().objects.filter(email=current_user).first()
    return render(request, 'main/pages/home.html', {'user': user})
   
def personal(request, personal: int):
    matching_personal = Personalsalud.objects.filter(hospitalid=personal).all()
    return render(request, 'main/personal.html', {'objects': matching_personal})

def consultas(request, personal: str):
    matching_consultas = Consulta.objects.filter(medConsulta=personal).all()
    return render(
        request=request,
        template_name='main/consultas.html',
        context={"objects": matching_consultas}
        )

def agregar_consulta(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        #FUNCION TRATAMIENTO DE DATOS PACIENTE
        processedData = process_data(file)
        #DATOS GENERALES
        processedDataPat = processedData[0]
        pat_id = processedDataPat['cedulapac']
        #DATOS MEDICOS
        processedDataReport = processedData[1]
        #FECHA
        fullDate = processedData[2]
        #LMP
        clinical_lmp = processedData[3]
        #MED NAME
        med_name = processedData[4]
        med_lastname = processedData[5]
        full_medName = med_name + " " + med_lastname
        
        onpatient = None
        last_report = None

        paciente_serializer = PacienteSerializer(data=processedDataPat)
        if paciente_serializer.is_valid():
            print("Guardar Paciente")
            paciente_serializer.save() #----> DESCOMENTAR PARA QUE SE GUARDE EL PACIENTE
            
        #Consulta en la tabla paciente y trae el userId para insertarlo en la tabla.
        onpatient = Paciente.objects.filter(cedulapac=pat_id).values_list('idpac', flat=True)[0]

        if onpatient is None:
            #return Response(status=status.HTTP_400_BAD_REQUEST)  
            raise MyCustomException("Algo ocurrió. No encontramos el paciente que buscas.")

        else:
            # ------------------- CREA LA HISTORIA CLÍNICA
            clinicHistory_info = {
                    'lmp': clinical_lmp,
                    'idPaciente': onpatient, #ARREGLAR MODELO
                }
            clinicHistory_serializer = HistoriaClinicaSerializer(data=clinicHistory_info)
            
            if clinicHistory_serializer.is_valid():
                print("Guardar Historia Clinica")
                clinicHistory_serializer.save() #----> DESCOMENTAR PARA QUE SE GUARDE LA HISTORIA
            
            # ------------------- CREA EL REPORTE CON LOS RESULTADOS
            reporte_serializer = ReporteSerializer(data=processedDataReport)
            if reporte_serializer.is_valid():
                print("Guardar Reporte")
                reporte_serializer.save() #----> DESCOMENTAR PARA QUE SE GUARDE EL REPORTE
                # Consulta en la tabla reporte y trae el Id del registro recién insertaado
                last_report = (Reporte.objects.last()).idreporte        
            
            # ------------------- CREA LA CONSULTA
            consulta_info = {
                'fecha_consulta': fullDate,
                'idpac': onpatient,
                'idreporte': last_report,
                'medUltrasonido': full_medName, #OJO, sólo se guardará la primera vez porque esto es un constraint unique. (TODO: MEJORAR LÓGICA)
            }
            
            print("aquí")
            consulta_serializer = ConsultaSerializer(data=consulta_info)
            if consulta_serializer.is_valid():
                #set_medico = (Personalsalud.objects.filter())
                print('Guarda Consulta. Fin del flujo. Eureka!')
                consulta_serializer.save() #----> DESCOMENTAR PARA GUARDAR CONSULTA
           
        return JsonResponse({"success": "true"})
    else:
        form = UploadFileForm()
    return render(
        request=request,
        template_name='consultas/agregar_consulta.html',
        context={"form": form}
    )