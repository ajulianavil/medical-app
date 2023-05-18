from django.urls import reverse
from main.models import *
from users.models import Appuser
from django.core.exceptions import PermissionDenied

def current_user(request):
    public_urls = [
        reverse('login'),
        reverse('landing'),
        reverse('aboutUs'),
        reverse('howToRegister')
    ]
    
    if request.path in public_urls:
        # Skip authentication check for the login page
        return {}
    
    if request.user.is_authenticated:
        user = request.user
        # Retrieve the relevant information from the user object or related models
        # Create a dictionary with the user information you need
        usuario = Appuser.objects.filter(email=user).first()
        if usuario:
            userid = usuario.userid
            userpass = usuario.password
            userrol = usuario.roles
            
            medico_data = Personalsalud.objects.filter(userid=userid).first()
            investigador_data = Usuarioexterno.objects.filter(userid=userid).first()
            print("asdsad0", investigador_data)
            if medico_data != None:
                nombre = medico_data.nombresmed
                apellido = medico_data.apellidosmed
                cedula = medico_data.cedulamed
                telefono = medico_data.telefonomed
                direccion = medico_data.direccionmed

            elif investigador_data != None:
                nombre = investigador_data.nombresext
                apellido = investigador_data.apellidosext
                cedula = investigador_data.cedulaext
                telefono = investigador_data.telefonoext
                direccion = investigador_data.direccionext
                                
            else:
                print("aun no hay informacion del usuario")
                nombre = ""
                apellido = ""
                cedula = ""
                telefono = ""
                direccion = ""                
            
            user_info = {
            'useremail': user.email,
            'userrol': userrol,
            'userid': userid,
            'userpassword': userpass,
            'user_name': nombre,
            'user_lastname': apellido,
            'user_identification': cedula,
            'user_phone': telefono,
            'user_address': direccion,
            }
            
            forbbiden_urls = [
                    reverse('consultas/nueva'),
                    reverse('registros'),
                    # reverse('registroinfo'),
                    # reverse('reporte_pdf'),
                    # reverse('reporte_graficos')
                ]
                
            if user_info['userrol'] == 'investigador':
                if request.path in forbbiden_urls:
                    raise PermissionDenied 
        
        else:
            print("Error no existe el usuario")
                
        return {'current_user': user_info}
    
    else:
        raise PermissionDenied("User not authenticated")

