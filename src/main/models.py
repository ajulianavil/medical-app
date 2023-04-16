from django.db import models
from django.utils import timezone

from users.models import Appuser
from .validators import val_cedulamed, val_cedulaext, val_cedulapac
# from tinymce.models import HTMLField

# Create your models here.
class Hospital(models.Model):
    nombrehospital = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=150)
    departamento = models.CharField(max_length=150)

    def __str__ (self):
        return self.nombrehospital
    
    class Meta:
        db_table = 'Hospital'
        verbose_name_plural = "Hospitales"
        ordering = ['nombrehospital']

class Personalsalud(models.Model):
    cedulamed = models.IntegerField( primary_key=True,)  # Field name made lowercase.
    nombresmed = models.CharField( max_length=150)  # Field name made lowercase.
    apellidosmed = models.CharField( max_length=150)  # Field name made lowercase.
    telefonomed = models.CharField(max_length=50,  unique=True)  # Field name made lowercase.
    direccionmed = models.CharField(max_length=200)  # Field name made lowercase.
    userid = models.ForeignKey(Appuser, on_delete=models.SET_DEFAULT, default="")  # Field name made lowercase.
    hospitalid = models.ForeignKey(Hospital, default="", verbose_name= "Hospitales", on_delete=models.SET_DEFAULT)  # Field name made lowercase.
    
    def __str__ (self):
        return str(self.cedulamed)
    
    class Meta:
        db_table = 'PersonalSalud'
        verbose_name_plural = "Personal"
        ordering = ['cedulamed']

class Reporte(models.Model):
    idreporte = models.AutoField(db_column='idReporte', primary_key=True)  # Field name made lowercase.
    efw = models.CharField(max_length=100, blank=True, null=True)
    edb = models.CharField(max_length=100, blank=True, null=True)
    ga = models.CharField(max_length=100, blank=True, null=True)
    csp_1 = models.CharField(max_length=50, blank=True, null=True)
    csp_avg = models.CharField(max_length=50, blank=True, null=True)
    cm_1 = models.CharField(max_length=50, blank=True, null=True)
    cm_avg = models.CharField(max_length=50, blank=True, null=True)
    hc_hadlock_1 = models.CharField(max_length=50, blank=True, null=True)
    hc_hadlock_avg = models.CharField(max_length=50, blank=True, null=True)
    hc_hadlock_ga = models.CharField(max_length=50, blank=True, null=True)
    hc_hadlock_edc = models.CharField(max_length=50, blank=True, null=True)
    hc_hadlock_dev = models.CharField(max_length=50, blank=True, null=True)
    bdp_hadlock_1 = models.CharField(max_length=50, blank=True, null=True)
    bdp_hadlock_avg = models.CharField(max_length=50, blank=True, null=True)
    bdp_hadlock_ga = models.CharField(max_length=50, blank=True, null=True)
    bdp_hadlock_edc = models.CharField(max_length=50, blank=True, null=True)
    bdp_hadlock_dev = models.CharField(max_length=50, blank=True, null=True)
    cereb_hill_1 = models.CharField(max_length=50, blank=True, null=True)
    cereb_hill_avg = models.CharField(max_length=50, blank=True, null=True)
    cereb_hill_ga = models.CharField(max_length=50, blank=True, null=True)
    cereb_hill_edc = models.CharField(max_length=50, blank=True, null=True)
    cereb_hill_dev = models.CharField(max_length=50, blank=True, null=True)
    va_1 = models.CharField(max_length=50, blank=True, null=True)
    va_avg = models.CharField(max_length=50, blank=True, null=True)
    vp_1 = models.CharField(max_length=50, blank=True, null=True)
    vp_avg = models.CharField(max_length=50, blank=True, null=True)
    ga_days = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Reporte'
        verbose_name_plural = "Reportes"

class Paciente(models.Model):
    idpac = models.AutoField(db_column='idPac', primary_key=True)  # Field name made lowercase.
    cedulapac = models.IntegerField(db_column='cedulaPac', blank=True, null=True, validators=[val_cedulapac], unique=True)  # Field name made lowercase.
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    nombreuno = models.CharField(db_column='nombreUno', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nombredos = models.CharField(db_column='nombreDos', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fechanac = models.CharField(db_column='fechaNac', max_length=100, blank=True, null=True)  # Field name made lowercase.
    numgestacion = models.IntegerField(db_column='numGestacion', blank=True, null=True)  # Field name made lowercase.

    class Meta: 
        verbose_name_plural = "Pacientes"
        db_table = 'Paciente'

class Historiaclinica(models.Model):
    idhistoriaclinica = models.AutoField(db_column='idHistoriaClinica', primary_key=True)  # Field name made lowercase.
    antquirurgico = models.TextField(db_column='antQuirurgico', blank=True, null=True)  # Field name made lowercase.
    antpatologico = models.TextField(db_column='antPatologico', blank=True, null=True)  # Field name made lowercase.
    antginecologico = models.TextField(db_column='antGinecologico', blank=True, null=True)  # Field name made lowercase.
    lmp = models.CharField(db_column='LMP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idPaciente = models.ForeignKey(Paciente, models.SET_DEFAULT, default="")  # Field name made lowercase.

    class Meta:
        db_table = 'HistoriaClinica'
        verbose_name_plural = "Historiales"

class Institucion(models.Model):
    institucionid = models.IntegerField(db_column='institucionId', primary_key=True)  # Field name made lowercase.
    nombreinstitucion = models.CharField(db_column='nombreInstitucion', max_length=150, blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(max_length=150, blank=True, null=True)
    departamento = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Instituciones"
        db_table = 'Institucion'

class Usuarioexterno(models.Model):
    cedulaext = models.IntegerField( primary_key=True, validators=[val_cedulaext])  # Field name made lowercase.
    nombresext = models.CharField( max_length=150, blank=True, null=True)  # Field name made lowercase.
    apellidosext = models.CharField( max_length=150, blank=True, null=True)  # Field name made lowercase.
    telefonoext = models.CharField( max_length=50, blank=True, null=True)  # Field name made lowercase.
    direccionext = models.CharField( max_length=200, blank=True, null=True)  # Field name made lowercase.
    userid = models.OneToOneField(Appuser, models.SET_DEFAULT, db_column='UserId', default="", unique=True)  # Field name made lowercase.
    institutionid = models.ForeignKey(Institucion, models.SET_DEFAULT, default="")  # Field name made lowercase.

    class Meta:
        verbose_name_plural = "UsuariosExternos"
        db_table = "UsuarioExterno"

class Consulta(models.Model):
    consultaid = models.AutoField(primary_key=True)
    fecha_consulta = models.DateTimeField()
    motivo_consulta = models.CharField(max_length=100, default='Ultrasonido de control')
    txtresults = models.CharField( max_length=100, blank=True, null=True)  # Field name made lowercase.
    medConsulta = models.ForeignKey(Personalsalud, models.SET_DEFAULT, default="", blank=True, null=True)
    medUltrasonido = models.CharField(max_length=200, blank=True, null=True)  # Field name made lowercase.# Field name made lowercase.
    idpac = models.ForeignKey(Paciente, models.SET_DEFAULT, default="")  # Field name made lowercase.
    idfeto = models.IntegerField( blank=True, null=True)  # Field name made lowercase.
    idreporte = models.OneToOneField(Reporte, models.SET_DEFAULT, unique=True, default="")  # Field name made lowercase.

    def __str__ (self):
        return str(self.consultaid)
    
    @property
    def consulta(self):
        return self.medConsulta.nombresmed + "/" + self.consultaid

    class Meta:
        db_table = 'Consulta'
        verbose_name_plural = "Consultas"
        ordering = ['consultaid']

        
class Tipomedicion(models.Model):
    idtipomedicion = models.AutoField(primary_key=True)  # Field name made lowercase.
    nombremedicion = models.CharField(max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'TipoMedicion'
        verbose_name_plural = "TiposMedicion"
        
class Medicion(models.Model):
    idmedicion = models.AutoField(db_column='id_medicion', primary_key=True)  # Field name made lowercase.
    id_tipo_medicion = models.ForeignKey(Tipomedicion, on_delete=models.SET_DEFAULT, default="")
    ga = models.IntegerField(db_column='ga', null=True)
    valormin = models.FloatField(db_column='valor_min', default=0.0, null=True, blank=True)  # Field name made lowercase.
    valormax = models.FloatField(db_column='valor_max', default=0.0, null=True, blank=True)  # Field name made lowercase.
    valorinter = models.FloatField(db_column='valor_inter', default=0.0, null=True, blank=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Medicion'
        verbose_name_plural = "Mediciones"
        


        





