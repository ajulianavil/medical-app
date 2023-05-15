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

from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, PageTemplate
from reportlab.graphics.shapes import Line, Drawing
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from ultrasonido_app.templatetags import my_filters
from reportlab.platypus.frames import Frame
from datetime import datetime


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
    
    matching_patient = Paciente.objects.filter(idpac=matching_consulta.idpac_id).first()
    
    matching_clinichist = Historiaclinica.objects.filter(idPaciente=matching_patient.idpac).first()

    matching_report = Reporte.objects.filter(idreporte=matching_consulta.idreporte_id).first()
    
    matching_result_info = FetoMedicionDiagnostico.objects.filter(reporte=matching_report.idreporte)

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
        fontSize=12,
        textColor='#0279AF'
    )
    
    val_style = ParagraphStyle(
        name='ValuesTitle',
        fontName='Helvetica-Bold',
        fontSize=10,
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
    ]
    
    # Information
    matching_consulta = Consulta.objects.filter(consultaid=idreporte_id).first()
    formatted_date = dt.strftime(matching_consulta.fecha_consulta, '%Y/%m/%d')
    formatted_hora = dt.strftime(matching_consulta.fecha_consulta, '%H:%M')
    matching_consulta.formatted_fecha_consulta = formatted_date
    matching_consulta.formatted_hora_consulta = formatted_hora
    
    matching_patient = Paciente.objects.filter(idpac=matching_consulta.idpac_id).first()
    
    matching_clinichist = Historiaclinica.objects.filter(idPaciente=matching_patient.idpac).first()

    matching_report = Reporte.objects.filter(idreporte=matching_consulta.idreporte_id).first()
    
    matching_result_info = FetoMedicionDiagnostico.objects.filter(reporte=matching_report.idreporte)
    
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
                            topMargin=50, bottomMargin=90)
    
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
    
    report_title = Paragraph('REPORTE MÉDICO N°{}'.format(idreporte_id), report_style)
    elements.append(report_title)
    title = Paragraph('ANOMALÍAS DEL SISTEMA NERVIOSO CENTRAL FETAL', title_style)
    elements.append(title)
    
    # Add a logo to the top corner of the document.
    # logo = Image('/static/images/logo_foscal.png', width=1.5*inch, height=1.5*inch)
    # logo.wrapOn(doc, 72, 72)
    # logo.drawOn(doc, doc.leftMargin, doc.height + doc.topMargin - logo.height)

    # Add a spacer to create a margin between the title and the logo.

    elements.append(spacer_logo)

     # Create a line drawing
    line_drawing = Drawing(400, 1)
    line_drawing.add(Line(0, 0, 500, 0))
    elements.append(line_drawing)
    
    elements.append(spacer_data)
    elements.append(Paragraph('DATOS DEL PACIENTE', section_title_style))
    elements.append(spacer_data)
    elements.append(line_drawing)
    elements.append(spacer_section)
    
    
    patient_data = [
    ["Fecha y hora de atención:", f"{formatted_date}" + " " + f"{formatted_hora}", "Médico encargado:", f"{matching_consulta.medUltrasonido}"],
    ["Paciente:", f"{matching_patient.nombreuno}" + " " + f"{matching_patient.apellido_paterno}", "Fecha est. de parto:", f"{matching_report.edb}"],
    ["Identificación:", f"{matching_patient.cedulapac}", "Edad gestacional:",  f"{matching_report.ga} semanas"],
    ["Fecha nacimiento:", f"{matching_patient.fechanac}", "Peso fetal:",  f"{matching_report.efw} gr"],
    ["Último periodo menstrual:", f"{matching_clinichist.lmp}"],    
    ]
    
    patientdata_table = Table(patient_data, style=table_style, colWidths=[2*inch, 1.5*inch, 2*inch, 1.5*inch])
    elements.append(patientdata_table)
    
    elements.append(spacer_section)
    elements.append(line_drawing)
    
        
    # SECCION ANTECEDENTES
    elements.append(spacer_data)
    elements.append(Paragraph('ANTECEDENTES', section_title_style))
    elements.append(spacer_data)
    elements.append(line_drawing)
    elements.append(spacer_section)
    elements.append(Paragraph('Antecedentes ginecológicos', val_style))
    elements.append(spacer_data)
    elements.append(Paragraph('{}.'.format(matching_clinichist.antginecologico), text_style))
    
    elements.append(spacer_subsection)
    elements.append(Paragraph('Antecedentes quirúrgicos', val_style))
    elements.append(spacer_data)
    elements.append(Paragraph('{}.'.format(matching_clinichist.antquirurgico), text_style))
    elements.append(spacer_data)
    
    elements.append(line_drawing)
    
    # SECCION OBSERVACIONES
    elements.append(spacer_section)
    elements.append(spacer_section)
    elements.append(Paragraph('OBSERVACIONES', section_title_style))
    
    elements.append(spacer_data)
    elements.append(Paragraph('El feto presenta valores normales en {} de {} mediciones.'.format(diagnostico['count'], diagnostico['num_fields']), text_style))
    elements.append(spacer_subsection)
    elements.append(Paragraph('Valores normales', val_style))
    elements.append(spacer_data)
    
    for med in diagnostico['normales']:
        nombre_medicion = my_filters.get_med_name(med)
        # valor_feto = my_filters.get_field_value(med)
        valor_feto = "hola"
        valor_ref = my_filters.get_ref_values(matching_report, med)
                
        elements.append(Paragraph('{}: El feto presenta un valor de {}, que se encuentra dentro del rango'
                                  .format(nombre_medicion, valor_ref), text_style))
        elements.append(spacer_data)
        
    elements.append(spacer_subsection)
    elements.append(Paragraph('Anormalidades', val_style))
    elements.append(spacer_data)
    
    for med in diagnostico['anormales']:
        nombre_medicion = my_filters.get_med_name(med)
        # valor_feto = my_filters.get_field_value(med)
        valor_feto = "hola"
        valor_ref = my_filters.get_ref_values(matching_report, med)
                
        elements.append(Paragraph('{}: El feto presenta un valor de {}, que se encuentra dentro del rango'
                                  .format(nombre_medicion, valor_ref), text_style))
        elements.append(spacer_data)
    
    elements.append(spacer_subsection)
    elements.append(Paragraph('Conclusiones', val_style))
    elements.append(spacer_data)
    
    
    
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
