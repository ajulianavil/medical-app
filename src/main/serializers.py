import datetime
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appuser 
        fields = ('userid', 'useremail', 'password', 'savedate', 'userroleid')
    
class PersonalSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personalsalud 
        fields = ('cedulamed', 'nombresmed', 'apellidosmed', 'telefonomed', 'direccionmed', 'userid', 'hospitalid')
        
class UsuarioExternoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarioexterno 
        fields = ('cedulaext', 'nombresext', 'apellidosext', 'telefonoext', 'direccionext', 'userid', 'institutionid')
        
class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'
        
class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta 
        fields = ('consultaid', 'fecha_consulta', 'motivo_consulta', 'txtresults', 'medConsulta', 'medUltrasonido', 'idpac', 'idfeto', 'idreporte')
        
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ('idpac', 'cedulapac', 'apellido_materno', 'apellido_paterno', 'nombreuno', 'nombredos', 'fechanac', 'numgestacion', 'lmp')
        
class HistoriaClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historiaclinica
        fields = '__all__'

class FetoMedicionDiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FetoMedicionDiagnostico
        fields =  'reporte', 'hc_hadlock', 'bpd_hadlock', 'csp', 'cm', 'vp', 'va', 'cereb_hill', 'efw', 'afi',