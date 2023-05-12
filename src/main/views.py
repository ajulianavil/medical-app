from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from main.forms import CreateUserForm, UploadFileForm
from .data_processing import comparison, process_data
from .Exceptions.PersonalizedExceptions import MyCustomException
from datetime import datetime as dt
from django.http import  JsonResponse
from main.models import *
from main.serializers import *
from django.contrib import messages

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
            
            consulta_serializer = ConsultaSerializer(data=consulta_info)
            if consulta_serializer.is_valid():
                #set_medico = (Personalsalud.objects.filter())
                print('Guarda Consulta. Fin del flujo. Eureka!')
                consulta_serializer.save() #----> DESCOMENTAR PARA GUARDAR CONSULTA

            # Aqui toca hacer que estos datos queden guardados en la bd
            diagnosis = comparison(processedDataReport)
            # for nombre in diagnosis["valores_normales"].keys():
            last_report = (Reporte.objects.last()).idreporte        
            #     feto_medicion_diagnostico = {
            #         'reporte': last_report,
            #         'nombre_valor': nombre,
            #         'diagnostico': diagnosis["valores_normales"][nombre][0],
            #         'valor_med': f'{diagnosis["valores_normales"][nombre][1]}',
            #         'valor_ref': diagnosis["valores_normales"][nombre][2],
            #     }
            diagnosis["reporte"] = last_report
            feto_medicion_diagnostico_serializer = FetoMedicionDiagnosticoSerializer(data=diagnosis)
            print(diagnosis)
            print('ISVALID', feto_medicion_diagnostico_serializer.is_valid())
            if feto_medicion_diagnostico_serializer.is_valid():
                print('entra')
                feto_medicion_diagnostico_serializer.save() #----> DESCOMENTAR PARA GUARDAR CONSULTA


        return JsonResponse({"success": "true"})
    else:
        form = UploadFileForm()
    return render(
        request=request,
        template_name='consultas/agregar_consulta.html',
        context={"form": form}
    )

def reporteInfo(request, param: int):
    print(param)
    matching_consulta = Consulta.objects.filter(consultaid=param).first()
    print(matching_consulta)
    formatted_date = dt.strftime(matching_consulta.fecha_consulta, '%Y/%m/%d')
    formatted_hora = dt.strftime(matching_consulta.fecha_consulta, '%H:%M')
    matching_consulta.formatted_fecha_consulta = formatted_date
    matching_consulta.formatted_hora_consulta = formatted_hora
    
    print("CONSULTAA", matching_consulta.consultaid)
    matching_patient = Paciente.objects.filter(idpac=matching_consulta.idpac_id).first()
    
    matching_clinichist = Historiaclinica.objects.filter(idPaciente=matching_patient.idpac).first()

    matching_report = Reporte.objects.filter(idreporte=matching_consulta.idreporte_id).first()
    
    print(matching_report.idreporte)
    matching_result_info = FetoMedicionDiagnostico.objects.filter(reporte=matching_report.idreporte)
    print("AAA", matching_result_info)
    count = 0
    num_fields = 0
    # for x in matching_result_info:
    #     if isinstance(x, FetoMedicionDiagnostico):
    #         print('hola',x)
    #         for field in x._meta.fields:
    #             num_fields = num_fields+1
                
    #             value = getattr(x, field.name)
    #             if value == 'Normal':
    #                 print(value)
    #                 count = count+1


    normal_columns = []
    anormales_columns = []

        # for field in instance._meta.fields:
        #     if getattr(instance, field.name) == 'Normal':
        #         normal_columns.append(field.name)
    for field in matching_result_info.get()._meta.fields:
        if getattr(matching_result_info.get(), field.name) == 'Normal':
            normal_columns.append(field.name)
        else:
            anormales_columns.append(field.name)
    
   
    print(type(matching_report))
    diagnostico = { 
            'form': matching_result_info,
            'num_fields': len(normal_columns) + len(anormales_columns[2:]), 
            'count': len(normal_columns),
            'normales':normal_columns,
            'anormales':anormales_columns[2:]
        }
    return render(request, 'reportes/reporte_info.html', context={"consulta": matching_consulta, "paciente": matching_patient, "clinicalhist": matching_clinichist, "reporte": matching_report, "diagnostico": diagnostico})

def repositorio(request):
    return render(request, 'repositorio/repositorio.html')

def reportes(request,):
    matching_consultas = Consulta.objects.all()
    return render(request, 'reportes/reportes.html', context={"objects": matching_consultas})


def agregar_usuario(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your form has been submitted successfully!')
            rol = request.GET.get('rol')
            form = CreateUserForm()
            return render(request, 'agregar_usuario/agregar_usuario_form.html', {"form": form, "rol": rol,})
        else:
            rol = request.GET.get('rol')
            return render(request, 'agregar_usuario/agregar_usuario_form.html', {"form": form, "rol": rol})
    else:
        rol = request.GET.get('rol')
        if rol:
            form = CreateUserForm()
            return render(request, 'agregar_usuario/agregar_usuario_form.html', {"form": form, "rol": rol})
        
        if not request.user.is_authenticated:
            return redirect('/login')   
        return render(request, 'agregar_usuario/seleccionar_usuario.html')


def consultas(request, personal: str):
    matching_consultas = Consulta.objects.filter(medConsulta=personal).all()
    return render(
        request=request,
        template_name='main/consultas.html',
        context={"objects": matching_consultas}
        )

def historia_clinica(request):
    return render(request, 'reportes/historia_clinica.html' )