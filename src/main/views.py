from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from main.forms import RepositorioFilterForm
from users.context_processors import current_user
from main.forms import CreateUserForm, UploadFileForm
from main.utils import get_matching_consulta, get_mediciones
from .data_processing import comparison, process_data
from .Exceptions.PersonalizedExceptions import MyCustomException
from datetime import datetime as dt
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

        if med_name == None or med_lastname == None:
            full_medName = None
        else:
            full_medName = med_name + " " + med_lastname
        
        onpatient = None
        last_report = 0
        last_consulta = 0

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
            reporte_serializer = ReporteSerializer(data=processedDataReport)
            if reporte_serializer.is_valid():
                try:
                    reporte = reporte_serializer.save() #----> DESCOMENTAR PARA QUE SE GUARDE EL REPORTE
                    last_report = reporte.idreporte
                except Exception as e:
                    messages.error(request, f"Error al guardar el reporte: {str(e)}")
                    paciente.delete()  # Delete the paciente record
                    return render(
                        request=request,
                        template_name='consultas/agregar_consulta.html',
                        context={"form": form}
                    )
                
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                paciente.delete()  # Delete the paciente record
                return render(
                    request=request,
                    template_name='consultas/agregar_consulta.html',
                    context={"form": form}
                )   
                
            # ------------------- CREA LA CONSULTA
            user_logged = current_user(request)
            info = list(user_logged.values())
            userid = info[0]['userid']
            
            med_consult = (Personalsalud.objects.filter(userid=userid)).first()
            if med_consult:
                med = med_consult.cedulamed
            
            consulta_info = {
                'fecha_consulta': fullDate,
                'idpac': onpatient,
                'idreporte': last_report,
                'medUltrasonido': full_medName, #OJO, sólo se guardará la primera vez porque esto es un constraint unique. (TODO: MEJORAR LÓGICA)
                'medConsulta': med
            }
            
            consulta_serializer = ConsultaSerializer(data=consulta_info)
            if consulta_serializer.is_valid():
                try:
                    consulta = consulta_serializer.save() #----> DESCOMENTAR PARA GUARDAR CONSULTA
                    last_consulta = consulta.consultaid
                except Exception as e:
                    messages.error(request, f"Error al guardar la consulta: {str(e)}")
                    paciente.delete()  # Delete the paciente record
                    reporte.delete()   # Delete the reporte record
                    return render(
                        request=request,
                        template_name='consultas/agregar_consulta.html',
                        context={"form": form}
                    )
                
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                paciente.delete()  # Delete the paciente record
                reporte.delete()   # Delete the reporte record
                return render(
                    request=request,
                    template_name='consultas/agregar_consulta.html',
                    context={"form": form}
                )

            diagnosis = comparison(processedDataReport)
            diagnosis["reporte"] = last_report
            
            feto_medicion_diagnostico_serializer = FetoMedicionDiagnosticoSerializer(data=diagnosis)
            
            if feto_medicion_diagnostico_serializer.is_valid():
                try:
                    feto_medicion_diagnostico_serializer.save()
                except Exception as e:
                    messages.error(request, f"Error al guardar el diagnóstico: {str(e)}")
                    paciente.delete()  # Delete the paciente record
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
                paciente.delete()  # Delete the paciente record
                reporte.delete()   # Delete the reporte record
                consulta.delete()  # Delete the consulta record
                return render(
                    request=request,
                    template_name='consultas/agregar_consulta.html',
                    context={"form": form}
                )
                    
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
    if request.method == 'POST':
    #     form = RepositorioFilterForm(request.POST)
    #     if form.is_valid():
    #         form.filter_results()
    #         messages.success(request, 'Resultados')
    #         # rol = request.GET.get('rol')
    #         form = RepositorioFilterForm()
    #         print("---------->>>>>>>", form)
    #         return render(request, 'repositorio/repositorio.html', {"objects": form})
    #     else:
    #         messages.error(request, 'Hay un problema.')
    #         return render(request, 'repositorio/repositorio.html', {"objects": form})
    # else:
    #     return render(request, 'repositorio/repositorio.html')
        # patced_input = request.POST.get('patced_input')
        # lastname_input = request.POST.get('lastname_input')
        ga_input = request.POST.get('ga_input') #reporte
        ga_input_final = request.POST.get('ga_input_final') #reporte
        state_input = request.POST.get('state_input') #diagnosis
        med_input = request.POST.get('med_input') #diagnosis
        diagnosis_input = request.POST.get('diagnosis_input') #diagnosis
        start_date = request.POST.get('start_date') #consulta
        end_date = request.POST.get('end_date') #consulta
        
        objects_list = []
        if ga_input == '':
            # matching_consultas = Consulta.objects.all()
            matching_consultas = Consulta.objects.all()
            
            for consulta in matching_consultas:
                consultaid = consulta.consultaid
                fecha_consulta = consulta.fecha_consulta
                motivo_consulta = consulta.motivo_consulta
                txtresults = consulta.txtresults
                medConsulta = consulta.medConsulta
                medUltrasonido = consulta.medUltrasonido
                paciente = consulta.idpac
                idfeto = consulta.idfeto
                idreporte = consulta.idreporte
                
                matching_paciente = Paciente.objects.filter(idpac=paciente.idpac)
                matching_reporte = Reporte.objects.filter(idreporte=idreporte.idreporte).first()
                matching_diagnostico = FetoMedicionDiagnostico.objects.filter(reporte=idreporte.idreporte)
                
                # Create a dictionary with the relevant data
                obj = {
                    'consulta': matching_consultas,
                    'paciente': matching_paciente,
                    'ga_reporte': matching_reporte.ga,
                    'report_date': fecha_consulta,
                    
                }
                    
                    # Append the dictionary to the objects list
                objects_list.append(obj)

            return render(request, 'repositorio/repositorio.html', context={"objects": objects_list})
        
        else:
            pacient = Paciente.objects.filter()
            print(pacient)
            if pacient:
                for item in pacient:
                    idpac = item.idpac
                    
                matching_records = Consulta.objects.filter(idpac=idpac)
                return render(request, 'reportes/reportes.html',  context={"objects": matching_records})
            else:
                messages.warning(request, f'No se encontraron coincidencias para el paciente de cédula')
                matching_consultas = Consulta.objects.all()
                return render(request, 'reportes/reportes.html', context={"objects": matching_consultas})
    else:
        return render(request, 'repositorio/repositorio.html')


def reportes(request,):
    user_logged = current_user(request)
    info = list(user_logged.values())
    userced = info[0]['user_identification']
    
    if request.method == 'POST':
        id_input = request.POST.get('id_input')
        if id_input == '':
            # matching_consultas = Consulta.objects.all()
            matching_consultas = Consulta.objects.filter(medConsulta=userced).order_by('-fecha_consulta')
            # -consultaid
            return render(request, 'reportes/reportes.html', context={"objects": matching_consultas})
        
        else:
            pacient = Paciente.objects.filter(cedulapac=id_input)
            print(pacient)
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
        matching_consultas = Consulta.objects.filter(medConsulta=userced).order_by('-fecha_consulta')
        return render(request, 'reportes/reportes.html', context={"objects": matching_consultas})

def reporte_graficos(request, idreporte_id:int ):
    matching_report = Reporte.objects.filter(idreporte=idreporte_id).first()
    print('matching_report')
    mediciones = get_mediciones().keys()
    return render(request, 'reportes/reporte_graficos.html', context ={"reporte": matching_report, "mediciones" : mediciones})

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
            messages.success(request, f'¡Se ha creado exitosamente el usuario para {form.cleaned_data["email"]}!')
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
    ["Fecha y hora de atención:", f"{matching_consulta.formatted_fecha_consulta}" + " " + f"{matching_consulta.formatted_hora_consulta}", "Médico encargado:", f"{matching_consulta.medUltrasonido}"],
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
    
    # elements.append(Paragraph('{}.'.format(matching_consulta.motivo_consulta), text_style))
        
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
            valor_feto = "hola"
            valor_ref = my_filters.get_ref_values(matching_report, med)
            
            diag_data.append([f"{nombre_medicion}", f"{valor_feto}", f"{valor_ref}"])
            
            diagdata_table = Table(diag_data, style=table_style, colWidths=[3.8*inch, 1.5*inch, 2*inch])
                
        # elements.append(Paragraph('{}: El feto presenta un valor de {}, que se encuentra dentro del rango'
        #                           .format(nombre_medicion, valor_ref), text_style))        
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
            # valor_feto = my_filters.get_field_value(med)
            valor_feto = "hola"
            valor_ref = my_filters.get_ref_values(matching_report, med)
            
            abnormal_data.append([f"{nombre_medicion}", f"{valor_feto}", f"{valor_ref}"])
            
            abnormal_data_table = Table(abnormal_data, style=table_style, colWidths=[3.8*inch, 1.5*inch, 2*inch])
        # elements.append(Paragraph('{}: El feto presenta un valor de {}, que se encuentra dentro del rango'
        #                           .format(nombre_medicion, valor_ref), text_style))
        # elements.append(spacer_data)
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
            # valor_feto = my_filters.get_field_value(med)
            valor_feto = "hola"
            valor_ref = my_filters.get_ref_values(matching_report, med)
            
            elements.append(Paragraph('{}: se encuentra fuera del rango {}, lo que puede indicar '
                                    .format(nombre_medicion, valor_ref), text_style))
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

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='my_pdf.pdf')

def editPacientData(request, consultaid: int):
    if request.method == 'POST':
        consulta = Consulta.objects.get(consultaid=consultaid)
        paciente = Paciente.objects.get(idpac=consulta.idpac.idpac)
        
        paciente.nombreuno = request.POST.get('name-uno')
        paciente.nombredos = request.POST.get('name-dos')
        paciente.apellido_paterno = request.POST.get('last-uno')
        paciente.apellido_materno = request.POST.get('last-dos')
        paciente.numgestacion = request.POST.get('gest')
        paciente.lmp = request.POST.get('lmp')
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
        print('hola ', parameter)
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
    
