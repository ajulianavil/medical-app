from django import template
from main.models import Personalsalud

register = template.Library()

@register.simple_tag
def get_medico_name(cedulamed):
    medico = Personalsalud.objects.get(cedulamed=cedulamed)
    first_name = medico.nombresmed.split(' ')[0] if ' ' in medico.nombresmed else medico.nombresmed
    last_name = medico.apellidosmed.split(' ')[0] if ' ' in medico.apellidosmed else medico.apellidosmed
    full_name = f'{first_name} {last_name}'
    return full_name  # Replace 'name' with the actual field you want to retrieve
