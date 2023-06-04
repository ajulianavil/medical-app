from django import template
from main.models import Personalsalud, Usuarioexterno, Hospital, Institucion
from users.models import Appuser

register = template.Library()

@register.simple_tag
def get_medico_name(cedulamed):
    medico = Personalsalud.objects.get(cedulamed=cedulamed)
    first_name = medico.nombresmed.split(' ')[0] if ' ' in medico.nombresmed else medico.nombresmed
    last_name = medico.apellidosmed.split(' ')[0] if ' ' in medico.apellidosmed else medico.apellidosmed
    full_name = f'{first_name} {last_name}'
    return full_name  # Replace 'name' with the actual field you want to retrieve

@register.simple_tag
def get_medico_id(cedulamed):
    medico = Personalsalud.objects.get(cedulamed=cedulamed).userid_id
    user = Appuser.objects.get(userid = medico)
    
    return user.userid  # Replace 'name' with the actual field you want to retrieve


@register.simple_tag
def get_info_user(userid):
    medico_data = Personalsalud.objects.filter(userid=userid).first()
    investigador_data = Usuarioexterno.objects.filter(userid=userid).first()
    cedula = None
    telefono = None
    direccion = None
    institucion = None
    
    if medico_data != None:
        cedula = medico_data.cedulamed
        telefono = medico_data.telefonomed
        direccion = medico_data.direccionmed
        institucion = Hospital.objects.get(id = medico_data.hospitalid_id).nombrehospital

    elif investigador_data != None:
        cedula = investigador_data.cedulaext
        telefono = investigador_data.telefonoext
        direccion = investigador_data.direccionext
        institucion = Institucion.objects.get(institucionid = investigador_data.institutionid_id).nombreinstitucion
    
    if cedula:
        return cedula, telefono, direccion, institucion  # Replace 'name' with the actual field you want to retrieve
    else:
        return '----'

# @register.simple_tag
# def get_info_user(userid):
