from django import template

from main.models import Medicion, Tipomedicion

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
        print('med', medicion)
        tipo_medicion = Tipomedicion.objects.get(nombreMedicion = medicion.upper())
        print('tipo_medicion', tipo_medicion)
        idMedicion = tipo_medicion.idTipoMedicion
        print('tipo_medicion', tipo_medicion.idTipoMedicion)
        print('idMedicion',idMedicion)
        if idMedicion == 1 or idMedicion == 2 or idMedicion == 7:
            med = Medicion.objects.get(id_tipo_medicion=idMedicion, ga=reporte.ga)
            return str(med.valormin) + ' - ' + str(med.valorinter)
        if idMedicion == 3: #CSP
            return 'X'
        if idMedicion == 4:
            return '10'
        if idMedicion == 5 or idMedicion == 6:
            if(medicion == 'va'):
                return 'va'
            if(medicion == 'vp'):
                return 'nose'
        if idMedicion == 8:
            return 'aaa'
    except Medicion.DoesNotExist:
        med = None
        print('medicion', medicion)
        print('report', reporte)
        print('tipo_medicion.idTipoMedicion', tipo_medicion.idTipoMedicion)
        return 'Nani'