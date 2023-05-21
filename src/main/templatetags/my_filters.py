import datetime
from django import template
from django.conf import settings
from users.context_processors import current_user

from main.models import *

register = template.Library()

@register.filter
def get_fields(obj):
    return obj._meta.get_fields()

@register.filter
def get_field_value(item, field):
    prefixed_attr = field + '_1'
    if hasattr(item, prefixed_attr):
        value = getattr(item, prefixed_attr)
        return value
    else:
        if hasattr(item, field):
            value = getattr(item, field)
            return value
        else:
            return None


@register.filter
def get_med_name(item):
    convertidorDeMediciones = {
        'hc_hadlock': 'Circunferencia de la cabeza (HC_HADLOCK)',
        'bpd_hadlock': 'Diámetro biparietal (BPD_HADLOCK)',
        'cereb_hill' : 'Diámetro transverso del cerebelo',
        'efw' : 'Peso estimado fetal',
        'csp': 'Cavum septumpellucidum',
        'cm':'Cisterna Magna (CM)',
        'vp':'Ventrículo posterior (VP)',
        'va':'Ventrículo anterior (VA)',
        'afi':'Indice de líquido amniótico (AFI)',
    }
    return convertidorDeMediciones[item]

@register.filter
def get_ref_values(reporte, medicion):
    try:
        tipo_medicion = Tipomedicion.objects.get(nombreMedicion = medicion.upper())
        idMedicion = tipo_medicion.idTipoMedicion
        med = Medicion.objects.get(id_tipo_medicion=idMedicion, ga=reporte.ga)

        if idMedicion == 1 or idMedicion == 2 or idMedicion == 7 or idMedicion == 3 or idMedicion == 9:
            return str(med.valormin) + ' - ' + str(med.valorinter)

        if idMedicion == 4:
            return settings.CM_REF
        
        if idMedicion == 5 or idMedicion == 6:
            if(medicion == 'va'):
                return 'va'
            if(medicion == 'vp'):
                return 'nose'
            
        if idMedicion == 8:
            
            return 'aaa'
        
    except Medicion.DoesNotExist:
        med = None
        return 'Nani'
    
@register.filter
def get_pacient_id(id:int):
    pacient = Paciente.objects.filter(idpac=id)
    if pacient:
        for item in pacient:
            idpac = item.cedulapac
        return idpac
    else:
        notFount = 'Sin cédula'
        return notFount                  
    
@register.filter
def total_pacientes(id:int):
    record_count = 0;
    current_month = datetime.datetime.now().month
    consulta_mes = Consulta.objects.filter(fecha_consulta__month=current_month, medConsulta=id)
    
    record_count = consulta_mes.count()
    return record_count

@register.filter
def total_fetos(id:int):
    record_count_normal = 0;
    
    current_month = datetime.datetime.now().month
    consulta_mes = Consulta.objects.filter(fecha_consulta__month=current_month, medConsulta=id)
    for consulta in consulta_mes:
        reporte = consulta.idreporte
        diagnostico = FetoMedicionDiagnostico.objects.filter(reporte = reporte)
        
        for field in diagnostico.get()._meta.fields:
            if getattr(diagnostico.get(), field.name) == 'Normal':
                record_count_normal += 1
                next
            else:
                break

    return record_count_normal

@register.filter
def total_anormales(id:int):
    record_count_anormal = 0;
    
    current_month = datetime.datetime.now().month
    consulta_mes = Consulta.objects.filter(fecha_consulta__month=current_month, medConsulta=id)
    for consulta in consulta_mes:
        reporte = consulta.idreporte
        diagnostico = FetoMedicionDiagnostico.objects.filter(reporte = reporte)
        
        for field in diagnostico.get()._meta.fields:
            if getattr(diagnostico.get(), field.name) == 'Normal':
                break
            else:
                record_count_anormal += 1
                break

    return record_count_anormal

@register.filter
def get_last_consult(id:int):
    consulta = Consulta.objects.filter(medConsulta=id).last()
    if consulta:
        return consulta
