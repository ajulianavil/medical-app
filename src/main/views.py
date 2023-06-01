from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from main.forms import RepositorioFilterForm
from users.context_processors import current_user
from main.forms import CreateUserForm, UploadFileForm
# from main.utils import get_matching_consulta, get_mediciones, export_to_csv
from main.utils import get_matching_consulta, get_mediciones
from .data_processing import comparison, process_data
from .Exceptions.PersonalizedExceptions import MyCustomException
from datetime import datetime as dt, timedelta
from django.http import  JsonResponse
from main.models import *
from main.serializers import *
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, PageTemplate
from reportlab.graphics.shapes import Line, Drawing
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from main.templatetags import my_filters
from reportlab.platypus.frames import Frame
from datetime import datetime
from django.templatetags.static import static
from reportlab.lib.colors import Color
import json
import math

from chartjs.views.lines import BaseLineChartView
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

    else:
        user_logged = current_user(request)
        info = list(user_logged.values())
        useremail = info[0]['useremail']
        userid = info[0]['userid']
        userrol = info[0]['userrol']

        user = get_user_model().objects.filter(email=useremail).first()

        if userrol == 'médico':
            is_register_complete = Personalsalud.objects.filter(userid=userid).all()
            if not is_register_complete:
                return redirect('user_data')
            
        if userrol == 'investigador':
            is_register_complete = Usuarioexterno.objects.filter(userid=userid).all()
            if not is_register_complete:
                return redirect('user_data')
        
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
#, embValue=None
def agregar_consulta(request):
    if request.method == 'POST':
        storage = messages.get_messages(request)
        storage.used = True
        form = UploadFileForm(request.POST, request.FILES)
        
        try:
            file = request.FILES['file']
        except:
            messages.error(request, 'Por favor seleccione un archivo')
            return render(
                request=request,
                template_name='consultas/agregar_consulta.html',
                context={"form": form}
            )

        if not file.name.endswith('.txt'):
            messages.error(request, 'Debe ingresar un archivo .txt')
            return render(
                    request=request,
                    template_name='consultas/agregar_consulta.html',
                    context={"form": form}
                )        
            
        #------------------------------------- FUNCION TRATAMIENTO DE DATOS PACIENTE
        processedData = process_data(file)
        
        processedDataPat = processedData[0]
        for key, value in processedDataPat.items():
            if value is None:
                messages.error(request, "El archivo no tiene información del paciente.")
                return render(
                request=request,
                template_name='consultas/agregar_consulta.html',
                context={"form": form}
            )
        pat_id = processedDataPat['cedulapac']
        
        processedDataReport = processedData[1]
        for key, value in processedDataReport.items():
            if value is None:
                messages.error(request, f"No encontramos información para '{key}'. Asegúrese de haber subido el archivo adecuado.")
                return render(
                request=request,
                template_name='consultas/agregar_consulta.html',
                context={"form": form}
            )
        
        #--------------------------------------------- DATOS GENERALES
        fullDate = processedData[2]
        med_name = processedData[3]
        med_lastname = processedData[4]
        comments = processedData[5]

        if med_name == None or med_lastname == None:
            full_medName = None
        else:
            full_medName = med_name + " " + med_lastname
        
        onpatient = None
        last_report = 0
        last_consulta = 0
        last_embarazo = 0
        consulta = None
        reporte = None

        paciente_serializer = PacienteSerializer(data=processedDataPat)
        if paciente_serializer.is_valid():
            try:
                paciente = paciente_serializer.save() #----> DESCOMENTAR PARA QUE SE GUARDE EL PACIENTE
            except Exception as e:
                messages.error(request, f"Error al guardar el paciente: {str(e)}")
                return render(
                    request=request,
                    template_name='consultas/agregar_consulta.html',
                    context={"form": form}
                )
        
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        
        #Consulta en la tabla paciente y trae el userId para insertarlo en la tabla.
        onpatient = Paciente.objects.filter(cedulapac=pat_id).values_list('idpac', flat=True)[0]

        if onpatient is None:
            #return Response(status=status.HTTP_400_BAD_REQUEST)  
            messages.error(request, f"No encontramos el paciente que buscas.")
            # paciente.delete()  # Delete the paciente record
            return render(
                    request=request,
                    template_name='consultas/agregar_consulta.html',
                    context={"form": form}
                )

        else:
            # ------------------- CREA EL EMBARAZO
            is_there_embarazo = Embarazo.objects.filter(idpac=onpatient).count()
            preg = processedDataPat["numgestacion"]
            
            # if is_there_embarazo == 0:
            if int(preg) > is_there_embarazo:
                embarazo_info = {
                    'idpac': onpatient,
                    'numero_embarazo': preg
                }
                embarazo_serializer = EmbarazoSerializer(data=embarazo_info)
                if embarazo_serializer.is_valid():
                    try:
                        embarazo = embarazo_serializer.save()
                        last_embarazo = embarazo.id_embarazo
                    except Exception as e:
                        messages.error(request, f"Error al guardar el embarazo: {str(e)}")
                        # Delete the paciente record
                        return render(
                            request=request,
                            template_name='consultas/agregar_consulta.html',
                            context={"form": form}
                        )
                else:
                    for error in list(form.errors.values()):
                        messages.error(request, error)
                    return render(
                        request=request,
                        template_name='consultas/agregar_consulta.html',
                        context={"form": form}
                    )
            else:
                #------- Si existe el embarazo obtenemos su id
                last_embarazo = Embarazo.objects.filter(idpac=onpatient, numero_embarazo = preg).first().id_embarazo

            # ------------------- CREA LA CONSULTA
            user_logged = current_user(request)
            info = list(user_logged.values())
            userid = info[0]['userid']
            userced = info[0]['user_identification']
            
            med_consult = (Personalsalud.objects.filter(userid=userid)).first()
            if med_consult:
                med = med_consult.cedulamed
            
            consulta_info = {
                'fecha_consulta': fullDate,
                'idpac': onpatient,
                # 'idreporte': last_report,
                'medUltrasonido': full_medName, #OJO, sólo se guardará la primera vez porque esto es un constraint unique. (TODO: MEJORAR LÓGICA)
                'medConsulta': med,
                'txtresults': comments
            }
            if last_embarazo:
                consulta_info['idembarazo'] = last_embarazo
            
            consulta_serializer = ConsultaSerializer(data=consulta_info)
            if consulta_serializer.is_valid():
                try:
                    consulta = consulta_serializer.save() #----> DESCOMENTAR PARA GUARDAR CONSULTA
                    last_consulta = consulta.consultaid
                except Exception as e:
                    messages.error(request, f"Error al guardar la consulta: {str(e)}")
                    return render(
                        request=request,
                        template_name='consultas/agregar_consulta.html',
                        context={"form": form}
                    )
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return render(
                    request=request,
                    template_name='consultas/agregar_consulta.html',
                    context={"form": form}
                )


            # ---------------- CREA EL REPORTE
            processedDataReport["consultaid"] = last_consulta
            reporte_serializer = ReporteSerializer(data=processedDataReport)
            if reporte_serializer.is_valid():
                print("================ si entre coño e la madre")
                try:
                    reporte = reporte_serializer.save() #----> DESCOMENTAR PARA QUE SE GUARDE EL REPORTE
                    last_report = reporte.idreporte
                except Exception as e:
                    messages.error(request, f"Error al guardar el reporte: {str(e)}")
                    consulta.delete()   # Delete the consulta record
                    return render(
                        request=request,
                        template_name='consultas/agregar_consulta.html',
                        context={"form": form}
                    )
                
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                consulta.delete()   # Delete the consulta record
                return render(
                    request=request,
                    template_name='consultas/agregar_consulta.html',
                    context={"form": form}
                )   
                
            
                
            # -------------------- CREA DIAGNOSTICO
            diagnosis = comparison(processedDataReport)
            diagnosis["reporte"] = last_report
            
            feto_medicion_diagnostico_serializer = FetoMedicionDiagnosticoSerializer(data=diagnosis)
            
            if feto_medicion_diagnostico_serializer.is_valid():
                try:
                    feto_medicion_diagnostico_serializer.save()
                except Exception as e:
                    messages.error(request, f"Error al guardar el diagnóstico: {str(e)}")
                    # Delete the paciente record
                    reporte.delete()   # Delete the reporte record
                    consulta.delete()  # Delete the consulta record
                    return render(
                        request=request,
                        template_name='consultas/agregar_consulta.html',
                        context={"form": form}
                    )
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                # Delete the paciente record
                reporte.delete()   # Delete the reporte record
                consulta.delete()  # Delete the consulta record
                return render(
                    request=request,
                    template_name='consultas/agregar_consulta.html',
                    context={"form": form}
                )
                    
        print('is_there_embarazo')
        print(is_there_embarazo)
        if is_there_embarazo > 0:
            print(is_there_embarazo)
            return redirect('paciente_existe', idpac=onpatient, consultaid=last_consulta)
        
        else:
            messages.success(request, "¡Se ha registrado correctamente al paciente en el sistema! De ahora en adelante podrá acceder a su historial clínico buscando su cédula en el módulo de 'Registros'.")
            target_url = reverse('registroinfo', args=[last_consulta])
            # Redirect to the target view
            return HttpResponseRedirect(target_url)

    else:
        form = UploadFileForm()
    return render(
        request=request,
        template_name='consultas/agregar_consulta.html',
        context={"form": form}
    )

def paciente_existe(request, idpac, consultaid):
    user_logged = current_user(request)
    info = list(user_logged.values())
    userced = info[0]['user_identification']
    
    if request.method == 'POST':
        last_consulta = request.POST.get('consulta')
        embarazo_id = request.POST.get('option')

        this_consulta = Consulta.objects.get(consultaid=last_consulta)

        if embarazo_id:
            if embarazo_id != '0':
                embarazo = Embarazo.objects.get(id_embarazo=int(embarazo_id))
                this_consulta.idembarazo_id = embarazo.id_embarazo
                
                this_consulta.save()
            else:
                embarazo_info = {
                    'idpac': idpac,
                }
                embarazo_serializer = EmbarazoSerializer(data=embarazo_info)
                if embarazo_serializer.is_valid():
                    # try:
                    embarazo = embarazo_serializer.save()
                    preg = embarazo.id_embarazo
                    
                this_consulta.idembarazo_id = embarazo.id_embarazo
                
                this_consulta.save()

        
        target_url = reverse('registroinfo', args=[last_consulta])
            # Redirect to the target view
        return HttpResponseRedirect(target_url)
    else:
        embarazos = Embarazo.objects.filter(idpac = idpac)
        embarazo_consultas = {}
        if embarazos:
            for embarazo in embarazos:
                consultas_embarazo = Consulta.objects.filter(idembarazo=embarazo.id_embarazo)
                embarazo_consultas[embarazo] = list(consultas_embarazo)

        paciente = Paciente.objects.get(idpac = idpac)
        last_consulta_meses = 0
        last_consulta_dias = 0
        try:
            #, medConsulta=userced
            consulta = Consulta.objects.filter(idpac = idpac).order_by('consultaid').reverse()[1]
            today = datetime.now().date()
            last_consulta = ((today - consulta.fecha_consulta.date()).days)/30
            last_consulta_meses = math.floor(last_consulta)  # Retrieves the whole number part
            last_consulta_dias = math.floor((last_consulta - last_consulta_meses)*30)
        except:
            consulta = None
            
        return render(request, 'reportes/paciente_existe.html', context={"paciente": paciente, "last_consulta": (last_consulta_meses, last_consulta_dias), "consulta": consultaid, "embarazo_consultas": embarazo_consultas})
        
def historial_paciente(request, idpac):
    embarazos = Embarazo.objects.filter(idpac = idpac)
    embarazo_consultas = {}
    if embarazos:
        for embarazo in embarazos:
            consultas_embarazo = Consulta.objects.filter(idembarazo=embarazo.id_embarazo)
            embarazo_consultas[embarazo] = list(consultas_embarazo)
                
    paciente = Paciente.objects.get(idpac=idpac)
    # consulta = Consulta.objects.filter(idpac=idpac).last()
    return render(request, 'consultas/historial_paciente.html', context={"paciente": paciente, "embarazos": embarazos, "embarazo_consultas": embarazo_consultas})

def resumen_embarazo(request, id_embarazo):
    embarazo = Embarazo.objects.get(id_embarazo=id_embarazo)
    embarazo_consultas = []
    
    consultas_embarazo = Consulta.objects.filter(idembarazo=id_embarazo)
    embarazo_consultas.append(consultas_embarazo) 

    return render(request, 'consultas/resumen_embarazo.html', context={"embarazo_consultas": embarazo_consultas, "embarazo": embarazo})

def reporteInfo(request, param: int):
    matching_consulta, matching_patient, matching_report, matching_result_info = get_matching_consulta(param)

    normal_columns = []
    anormales_columns = []

    for field in matching_result_info.get()._meta.fields:
        if getattr(matching_result_info.get(), field.name) == 'Normal':
            normal_columns.append(field.name)
        else:
            anormales_columns.append(field.name)

    diagnostico = { 
            'form': matching_result_info,
            'num_fields': len(normal_columns) + len(anormales_columns[2:]), 
            'count': len(normal_columns),
            'normales':normal_columns,
            'anormales':anormales_columns[2:]
        }
    
    return render(request, 'reportes/reporte_info.html', context={"consulta": matching_consulta, "paciente": matching_patient, "reporte": matching_report, "diagnostico": diagnostico})

def repositorio(request):
    objects_list = []

    if request.method == 'POST':
        ga_input = request.POST.get('ga_input')
        ga_input_final = request.POST.get('ga_input_final')
        med_input = request.POST.get('med_input')
        diagnosis_input = request.POST.get('diagnosis_input')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        filter_kwargs = {}
        if med_input != "todas":
            filter_kwargs[med_input] = diagnosis_input
        matching_consultas = Consulta.objects.filter(fecha_consulta__range=(start_date, end_date))
        for consulta in matching_consultas:
            matching_reporte = Reporte.objects.filter(consultaid=consulta.consultaid, ga__range=(ga_input, ga_input_final)).first()
            if matching_reporte is not None:
                diagnostico = FetoMedicionDiagnostico.objects.filter(reporte=matching_reporte.idreporte,**filter_kwargs).first()
                if diagnostico is not None:
                # if datetime.strptime(start_date, '%Y-%m-%d') < consulta.fecha_consulta < datetime.strptime(end_date, '%Y-%m-%d'):
                    obj = {
                        'reporte': matching_reporte,
                        # 'paciente': matching_paciente,
                        'diagnostico': diagnostico,
                        'ga_reporte': matching_reporte.ga,
                        'report_date': consulta.fecha_consulta,
                    }

                    objects_list.append(obj)
                #Append the dictionary to the objects list
        
        filter_kwargs["ga_input"] = ga_input
        filter_kwargs["ga_input_final"] = ga_input_final
        filter_kwargs["start_date"] = start_date
        filter_kwargs["end_date"] = end_date
        filter_kwargs["med_input"] = med_input
        filter_kwargs["diagnosis_input"] = diagnosis_input
        print(filter_kwargs)
        return render(request, 'repositorio/repositorio.html', context={"objects": objects_list, "filtros": filter_kwargs})
        
    else:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=90)
        matching_consultas = Consulta.objects.filter(fecha_consulta__range=(start_date, end_date)).order_by('-fecha_consulta')
        
        for consulta in matching_consultas:
            matching_reporte = Reporte.objects.filter(idreporte=consulta.idreporte_id).first()
            diagnostico = FetoMedicionDiagnostico.objects.filter(reporte_id=consulta.idreporte_id).first()
            obj = {
                'reporte': matching_reporte,
                'diagnostico': diagnostico,
                'ga_reporte': matching_reporte.ga,
                'report_date': consulta.fecha_consulta,  
            }
            
            # Append the dictionary to the objects list
            objects_list.append(obj)

        return render(request, 'repositorio/repositorio.html', context={"objects": objects_list})


def reportes(request,):
    user_logged = current_user(request)
    info = list(user_logged.values())
    userced = info[0]['user_identification']
    date_end = datetime.now().date()
    date_init = date_end - timedelta(days=30)
    
    if request.method == 'POST':
        id_input = request.POST.get('id_input')
        if id_input == '':
            # matching_consultas = Consulta.objects.filter(medConsulta=userced).order_by('-fecha_consulta')
            matching_consultas = Consulta.objects.filter(medConsulta=userced, fecha_consulta__range=(date_init, date_end)).order_by('-fecha_consulta')

            return render(request, 'reportes/reportes.html', context={"objects": matching_consultas})
        
        else:
            pacient = Paciente.objects.filter(cedulapac=id_input)
            if pacient:
                for item in pacient:
                    idpac = item.idpac
                    
                matching_records = Consulta.objects.filter(idpac=idpac, medConsulta=userced).order_by('-fecha_consulta')
                return render(request, 'reportes/reportes.html',  context={"objects": matching_records})
            else:
                messages.warning(request, f'No se encontraron coincidencias para el paciente de cédula {id_input}')
                matching_consultas = Consulta.objects.filter(medConsulta=userced).order_by('-fecha_consulta')
                return render(request, 'reportes/reportes.html', context={"objects": matching_consultas})
    else:
        matching_consultas = Consulta.objects.filter(medConsulta=userced, fecha_consulta__range=(date_init, date_end)).order_by('-fecha_consulta')
        return render(request, 'reportes/reportes.html', context={"objects": matching_consultas})

def reporte_graficos(request, consultaid:int):
    matching_report = Reporte.objects.filter(consultaid=consultaid).first()
    matching_consulta = Consulta.objects.get(consultaid=consultaid)
    mediciones = get_mediciones()
    
    mediciones_dict = {
        'hc_hadlock': 1,
        'bpd_hadlock': 2,
        'csp': 3,
        'cm': 4,
        'vp': 5,
        'va': 6,
        'cereb_hill': 7,
        'afi': 8,
        'efw': 9
    }
    
    reporte_data = {}

    for med, med_id in mediciones_dict.items():
        if med_id != 8:
            medvalue = Medicion.objects.get(ga=matching_report.ga, id_tipo_medicion=med_id)
            
            column_mapping = {
                'hc_hadlock': 'hc_hadlock_1',
                'bpd_hadlock': 'bpd_hadlock_1',
                'csp': 'csp_1',
                'cm': 'cm_1',
                'vp': 'vp_1',
                'va': 'va_1',
                'cereb_hill': 'cereb_hill_1',
                'afi': 'afi',
                'efw': 'efw',
            }

            # reporte_data = {med: getattr(matching_report, column_mapping.get(med, med)) for med in mediciones_dict.keys()}
            if med not in reporte_data:
                reporte_data[med] = {
                    'value': getattr(matching_report, column_mapping.get(med, med)),
                    'minvalue': medvalue.valormin,
                    'maxvalue': medvalue.valorinter,
                }
    
    return render(request, 'reportes/reporte_graficos.html', context ={"reporte": matching_report, "mediciones" : mediciones_dict, "reporte_data": reporte_data, "matching_consulta": matching_consulta})

def chart_data_view(request, idreporte_id:int, nombreMedicion:str, ga: str):
    mediciones = get_mediciones()
    # value_reporte = my_filters.get_field_value(nombreMedicion)
    valores_medicion = Medicion.objects.filter(id_tipo_medicion=mediciones[nombreMedicion])
    matching_report = Reporte.objects.filter(idreporte=idreporte_id).first()
    value_reporte = my_filters.get_field_value(matching_report,nombreMedicion)

    values_min = [result.valormin for result in valores_medicion]
    values_max = [result.valorinter for result in valores_medicion]
    values_ga = [result.ga for result in valores_medicion]
    data = {
        'values_min': values_min,
        'values_max': values_max,
        'values_ga': values_ga,
        'ga_reporte': ga,
        'value_reporte': value_reporte
    }

    # Return the updated chart data as a JSON response
    return JsonResponse(data, safe=False)


def agregar_usuario(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'¡Se ha creado exitosamente el usuario para {form.cleaned_data["email"]}! Por favor indíquele al usuario que ingrese y actualice su contraseña.')
            rol = request.GET.get('rol')
            form = CreateUserForm()
            return render(request, 'agregar_usuario/agregar_usuario_form.html', {"form": form, "rol": rol})
        else:
            # messages.error(request, errorlist)
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

def ver_usuarios(request):
    
    if request.method == 'POST':
        all_users = Appuser.objects.all().order_by('-savedate')
        # id_input = request.POST.get('id_input')
        email_input = request.POST.get('email_input')
        
        if email_input == '':
            return render(request, 'agregar_usuario/ver_usuarios.html',  context={"objects": all_users})
            
        else:
            usuario = Appuser.objects.get(email=email_input)
            if usuario:
                all_users = [usuario] 
                return render(request, 'agregar_usuario/ver_usuarios.html',  context={"objects": all_users})
            else:
                messages.warning(request, f'No existe usuario con el email {email_input}')
                return render(request, 'agregar_usuario/ver_usuarios.html', context={"objects": all_users})
        # if id_input == '' and email_input == '':
        #     for user in all_users:
        #         try:
        #             personal_salud = Personalsalud.objects.get(userid=user.userid)
        #             user.userced = personal_salud.cedulamed
        #         except Personalsalud.DoesNotExist:
        #             try:
        #                 usuario_externo = Usuarioexterno.objects.get(userid=user.userid)
        #                 user.userced = usuario_externo.cedulaext
        #             except Usuarioexterno.DoesNotExist:
        #                 user.userced = None

        #     return render(request, 'agregar_usuario/ver_usuarios.html',  context={"objects": all_users})
        
        # else:
        #     if email_input != '' and id_input == '':
        #         usuario = Appuser.objects.get(email=email_input)
                
        #         user = Personalsalud.objects.get(userid=usuario.userid) or Usuarioexterno.objects.get(userid=usuario.userid)
        #         userid = 0
        #         userced = 0
                
        #         if user.userid:
        #             userid = user.userid.userid
        #             if user.cedulamed:
        #                 userced = user.cedulamed
        #             elif user.cedulaext:
        #                 userced = user.cedulaext
                
        #         if userid != 0:
        #             usuario.userced = userced
        #             all_users = [usuario] 
        #             if usuario:
        #                 return render(request, 'agregar_usuario/ver_usuarios.html',  context={"objects": all_users})
        #             else:
        #                 messages.warning(request, f'No existe usuario con el correo {email_input}')
        #                 return render(request, 'agregar_usuario/ver_usuarios.html', context={"objects": all_users})
                
        #         else:
        #             messages.warning(request, f'No existe usuario con el email {email_input}')
        #             return render(request, 'agregar_usuario/ver_usuarios.html', context={"objects": all_users})

        #     elif email_input == '' and id_input != '':
        #         user = Personalsalud.objects.get(cedulamed=id_input) or Usuarioexterno.objects.get(cedulaext=id_input)
        #         userid = 0
        #         userced = 0
                
        #         if user.userid:
        #             userid = user.userid.userid
        #             if user.cedulamed:
        #                 userced = user.cedulamed
        #             elif user.cedulaext:
        #                 userced = user.cedulaext
                
        #         if userid != 0:
        #             usuario = Appuser.objects.get(userid=userid)
        #             usuario.userced = userced
        #             all_users = [usuario] 

        #             if usuario:
        #                 return render(request, 'agregar_usuario/ver_usuarios.html',  context={"objects": all_users})
        #             else:
        #                 messages.warning(request, f'Ocurrió un error al buscar la cédula {id_input}')
        #                 return render(request, 'agregar_usuario/ver_usuarios.html', context={"objects": all_users})
                    
        #         else:
        #             messages.warning(request, f'No existe usuario con la cédula {id_input}')
        #             return render(request, 'agregar_usuario/ver_usuarios.html', context={"objects": all_users})
                
        #     elif email_input != '' and id_input != '':
        #         user = Personalsalud.objects.get(cedulamed=id_input) or Usuarioexterno.objects.get(cedulaext=id_input)
        #         userid = 0
        #         userced = 0
                
        #         if user.userid:
        #             userid = user.userid.userid
        #             if user.cedulamed:
        #                 userced = user.cedulamed
        #             elif user.cedulaext:
        #                 userced = user.cedulaext
                
        #         if userid != 0:
        #             usuario = Appuser.objects.get(userid=userid, email=email_input)
        #             usuario.userced = userced
        #             all_users = [usuario]  
                            
        #             if usuario:
        #                 return render(request, 'agregar_usuario/ver_usuarios.html',  context={"objects": all_users})
        #             else:
        #                 messages.warning(request, f'Ocurrió un error al buscar la cédula {id_input} o el correo {email_input}')
        #                 return render(request, 'agregar_usuario/ver_usuarios.html', context={"objects": all_users})
                    
        #         else:
        #             messages.warning(request, f'No existe usuario con la cédula {id_input} o el correo {email_input}')
        #             return render(request, 'agregar_usuario/ver_usuarios.html', context={"objects": all_users})
    
    else:
        all_users = Appuser.objects.all().order_by('-savedate')
        # for user in all_users:
        #         try:
        #             personal_salud = Personalsalud.objects.get(userid=user.userid)
        #             user.userced = personal_salud.cedulamed
        #         except Personalsalud.DoesNotExist:
        #             try:
        #                 usuario_externo = Usuarioexterno.objects.get(userid=user.userid)
        #                 user.userced = usuario_externo.cedulaext
        #             except Usuarioexterno.DoesNotExist:
        #                 user.userced = None
        return render(request, 'agregar_usuario/ver_usuarios.html',  context={"objects": all_users})

def deactivateUser(request, userid):
    user = Appuser.objects.get(userid=userid)
    user.is_active = False
    user.save()
    
    all_users = Appuser.objects.all().order_by('-savedate')
    return render(request, 'agregar_usuario/ver_usuarios.html',  context={"objects": all_users})

def reactivateUser(request, userid):
    user = Appuser.objects.get(userid=userid)
    user.is_active = True
    user.save()
    
    all_users = Appuser.objects.all().order_by('-savedate')
    return render(request, 'agregar_usuario/ver_usuarios.html',  context={"objects": all_users})



def consultas(request, personal: str):
    matching_consultas = Consulta.objects.filter(medConsulta=personal).all()
    return render(
        request=request,
        template_name='main/consultas.html',
        context={"objects": matching_consultas}
        )

def historia_clinica(request):
    return render(request, 'reportes/historia_clinica.html' )

def footer(canvas, doc):
    # Define a style for the text
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica-Bold"
    style.fontSize = 8
    style.textColor = colors.black
    
    # Add your footer content here
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    x1, y1 = 50, 90
    x2, y2 = 560, 90
    canvas.line(x1, y1, x2, y2)
    # Set the font and draw the text with the current date and time
    canvas.setFont(style.fontName, style.fontSize)
    canvas.setFillColor(style.textColor)
    canvas.drawString(18*mm, 20*mm, f"Fecha y hora de impresión: {current_date}")

def reporte_pdf(request, idreporte_id: int):
    buf = io.BytesIO()
    
    # Styles
    # Define a custom ParagraphStyle
    report_style = ParagraphStyle(
        name='CustomTitleReport',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=18,
        spaceAfter=2*mm,
        textColor='#0279AF'
        )
    
    title_style = ParagraphStyle(
        name='CustomTitle',
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor='#0279AF'
    )
    
    section_title_style = ParagraphStyle(
        name='ObservationsTitle',
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor='#0279AF'
    )
    
    val_style = ParagraphStyle(
        name='ValuesTitle',
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor='#0279AF'
    )
    
    text_style = ParagraphStyle(
        name='TextTitle',
        fontName='Helvetica',
        fontSize=10,
    )
    
    # Define the style for the table cells
    table_style = [
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]
    
    table_med_style = [
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTWEIGHT', (0, 0), (-1, -1), 'BOLD'),  # Make the font bold
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]
    
    # Information
    matching_consulta, matching_patient, matching_report, matching_result_info = get_matching_consulta(idreporte_id)

    medico = Personalsalud.objects.get(cedulamed=matching_consulta.medConsulta_id)
    first_name = medico.nombresmed.split(' ')[0] if ' ' in medico.nombresmed else medico.nombresmed
    last_name = medico.apellidosmed.split(' ')[0] if ' ' in medico.apellidosmed else medico.apellidosmed
    full_name = f'{first_name} {last_name}'
    normal_columns = []
    anormales_columns = []

    for field in matching_result_info.get()._meta.fields:
        if getattr(matching_result_info.get(), field.name) == 'Normal':
            normal_columns.append(field.name)
        else:
            anormales_columns.append(field.name)

    diagnostico = { 
            'form': matching_result_info,
            'num_fields': len(normal_columns) + len(anormales_columns[2:]), 
            'count': len(normal_columns),
            'normales':normal_columns,
            'anormales':anormales_columns[2:]
        }
    
    doc = SimpleDocTemplate(buf, pagesize=letter,
                            rightMargin=40, leftMargin=50,
                            topMargin=20, bottomMargin=90)
    
     # Create a list to hold the flowables.
    elements = []
    
    spacer_logo = Spacer(1, 0.25*inch)
    spacer_section = Spacer(1, 0.18*inch)
    spacer_subsection = Spacer(1, 0.23*inch)
    spacer_data = Spacer(1, 0.15*inch)

    # Add a title to the document.
    styles = getSampleStyleSheet()
    
    max_height = 7 * inch  # adjust the value as needed
    current_height = 0
    
    report_title = Paragraph('REPORTE MÉDICO N°{}'.format(matching_report.idreporte), report_style)
    elements.append(report_title)
    title = Paragraph('ANOMALÍAS DEL SISTEMA NERVIOSO CENTRAL FETAL', title_style)
    elements.append(title)
    
    image = Image('main/static/images/logo_foscal.png', width=1.5*inch, height=0.8*inch, hAlign="LEFT")
    elements.insert(0,image)

    elements.append(spacer_logo)

     # Create a line drawing
    line_drawing = Drawing(400, 1)
    line = Line(0, 0, 500, 0)
    line.strokeColor = Color(0.851, 0.851, 0.851)
    line_drawing.add(line)
    elements.append(line_drawing)
    
    elements.append(spacer_data)
    elements.append(Paragraph('DATOS DEL PACIENTE', section_title_style))
    elements.append(spacer_data)
    elements.append(line_drawing)
    elements.append(spacer_section)
    
    patient_data = [
    ["Fecha y hora de atención:", f"{matching_consulta.formatted_fecha_consulta}" + " " + f"{matching_consulta.formatted_hora_consulta}", "Médico encargado:", f"{full_name}"],
    ["Paciente:", f"{matching_patient.nombreuno}" + " " + f"{matching_patient.apellido_paterno}", "Fecha est. de parto:", f"{matching_report.edb}"],
    ["Identificación:", f"{matching_patient.cedulapac}", "Edad gestacional:",  f"{matching_report.ga} semanas"],
    ["Peso fetal:",  f"{matching_report.efw} gr", "Último periodo menstrual:", f"{matching_patient.lmp}"],
    ]
    
    patientdata_table = Table(patient_data, style=table_style, colWidths=[2*inch, 1.5*inch, 2*inch, 1.5*inch])
    elements.append(patientdata_table)
    
    motivo_consulta = [
    ["Motivo consulta:", matching_consulta.motivo_consulta],    
    ]
    elements.append(spacer_data)
    motivo_consulta_table = Table(motivo_consulta, style=table_style, colWidths=[1.5*inch, 5.5*inch])
    elements.append(motivo_consulta_table)
            
    elements.append(spacer_section)
    elements.append(line_drawing)
        
    # SECCION OBSERVACIONES
    elements.append(spacer_section)
    elements.append(spacer_section)
    elements.append(Paragraph('RESULTADOS', section_title_style))
    
    elements.append(spacer_data)
    elements.append(Paragraph('El feto presenta valores normales en {} de {} mediciones.'.format(diagnostico['count'], diagnostico['num_fields']), text_style))
    elements.append(spacer_subsection)
    elements.append(Paragraph('Valores normales', val_style))
    elements.append(spacer_data)
    
    med_data = ["MEDICIÓN", "VALOR", "REFERENCIA"],    
    med_data_table = Table(med_data, style=table_med_style, colWidths=[3.8*inch, 1.5*inch, 2*inch])
    
    if len(diagnostico['normales']) == 0:
        elements.append(Paragraph('El feto no presenta valores normales que correspondan a su edad gestacional.', text_style))
    else:
        diag_data = []
        for med in diagnostico['normales']:
            nombre_medicion = my_filters.get_med_name(med)
            # valor_feto = my_filters.get_field_value(med)
            valor_feto = my_filters.get_field_value(matching_report, med)

            valor_ref = my_filters.get_ref_values(matching_report, med)
            
            diag_data.append([f"{nombre_medicion}", f"{valor_feto}", f"{valor_ref}"])
            
            diagdata_table = Table(diag_data, style=table_style, colWidths=[3.8*inch, 1.5*inch, 2*inch])
                       
        elements.append(med_data_table)
        elements.append(diagdata_table)
    
    elements.append(spacer_subsection)
    elements.append(Paragraph('Anormalidades', val_style))
    elements.append(spacer_data)
    
    abnormal_data = []
    if len(diagnostico['anormales']) == 0:
        elements.append(Paragraph('El feto no presenta anormalidades', text_style))
        
    else:
        for med in diagnostico['anormales']:
            nombre_medicion = my_filters.get_med_name(med)
            valor_feto = my_filters.get_field_value(matching_report, med)
            valor_ref = my_filters.get_ref_values(matching_report, med)
            
            abnormal_data.append([f"{nombre_medicion}", f"{valor_feto}", f"{valor_ref}"])
            
            abnormal_data_table = Table(abnormal_data, style=table_style, colWidths=[3.8*inch, 1.5*inch, 2*inch])

        elements.append(med_data_table)
        elements.append(abnormal_data_table)
    
    elements.append(spacer_subsection)
    elements.append(Paragraph('Conclusiones', val_style))
    elements.append(spacer_data)
    
    if len(diagnostico['anormales']) == 0:
        elements.append(Paragraph('El feto está dentro de los rangos normales para su edad gestacional.', text_style))
    else:
        for med in diagnostico['anormales']:
            nombre_medicion = my_filters.get_med_name(med)
            valor_ref = my_filters.get_ref_values(matching_report, med)
            diag = my_filters.get_diagnosis(matching_report, med)
            
            
            elements.append(Paragraph('{}: se encuentra fuera del rango {}, lo que puede indicar {}'
                                    .format(nombre_medicion, valor_ref, diag), text_style))
            elements.append(spacer_data)
    
    if matching_consulta.txtresults != None:
        elements.append(spacer_subsection)
        elements.append(Paragraph('OBSERVACIONES DEL MÉDICO', section_title_style))
        elements.append(spacer_data)
        elements.append(Paragraph('{}'.format(matching_consulta.txtresults), text_style))
    
    #Footer
    # Define the page template with the footer
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    template = PageTemplate(id='test', frames=[frame], onPage=footer)
    doc.addPageTemplates([template])

    
    # Build the document and render the PDF.
    doc.build(elements)

    buf.seek(0)
    filename = 'REPORTE_{}_{}.pdf'.format(datetime.now().strftime('%Y%m%d'), matching_patient.cedulapac)

    return FileResponse(buf, as_attachment=True, filename=filename)

def editPacientData(request, consultaid: int):
    if request.method == 'POST':
        consulta = Consulta.objects.get(consultaid=consultaid)
        paciente = Paciente.objects.get(idpac=consulta.idpac.idpac)
        
        if request.POST.get('name-uno') != "":
            paciente.nombreuno = request.POST.get('name-uno')
        if request.POST.get('name-dos') != "":
            paciente.nombredos = request.POST.get('name-dos')
        if request.POST.get('last-uno') != "":
            paciente.apellido_paterno = request.POST.get('last-uno')
        if request.POST.get('last-dos') != "":
            paciente.apellido_materno = request.POST.get('last-dos')
        # if request.POST.get('gest') != "":
        #     paciente.numgestacion = request.POST.get('gest')
        # if request.POST.get('lmp') != "":
        #     paciente.lmp = request.POST.get('lmp')

        consulta.motivo_consulta = request.POST.get('motivo')
        
        paciente.save()
        consulta.save()
        target_url = reverse('registroinfo', args=[consultaid])
        return HttpResponseRedirect(target_url)
    
def editReportData(request, consultaid: int):
    if request.method == 'POST':
        consulta = Consulta.objects.get(consultaid=consultaid)
        consulta.txtresults = request.POST.get('obs')
        consulta.save()

        target_url = reverse('registroinfo', args=[consultaid])
        return HttpResponseRedirect(target_url)

def get(self, request, *args, **kwargs):
        parameter = request.GET.get('parameter')
        if parameter == 'example1':
            data = {
                'labels': ["January", "February", "March", "April", "May", "June", "July"],
                'datasets': [
                    [75, 44, 92, 11, 44, 95, 35],
                    [41, 92, 18, 3, 73, 87, 92],
                    [87, 21, 94, 3, 90, 13, 65]
                ]
            }
        elif parameter == 'example2':
            data = {
                'labels': ["January", "February", "March", "April", "May", "June", "July"],
                'datasets': [
                    [50, 60, 70, 80, 90, 100, 110],
                    [20, 30, 40, 50, 60, 70, 80],
                    [10, 20, 30, 40, 50, 60, 70]
                ]
            }
        else:
            data = {
                'labels': ["January", "February", "March", "April", "May", "June", "July"],
                'datasets': [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]
                ]
            }

        return JsonResponse(data)
    
