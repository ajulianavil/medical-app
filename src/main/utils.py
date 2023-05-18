from datetime import datetime

from main.models import *

def get_matching_consulta(consulta_id):
    print(consulta_id)
    matching_consulta = Consulta.objects.filter(consultaid=consulta_id).first()
    formatted_date = datetime.strftime(matching_consulta.fecha_consulta, '%Y/%m/%d')
    formatted_hora = datetime.strftime(matching_consulta.fecha_consulta, '%H:%M')
    matching_consulta.formatted_fecha_consulta = formatted_date
    matching_consulta.formatted_hora_consulta = formatted_hora
    matching_patient = Paciente.objects.filter(idpac=matching_consulta.idpac_id).first()
    matching_clinichist = Historiaclinica.objects.filter(idPaciente=matching_patient.idpac).first()
    matching_report = Reporte.objects.filter(idreporte=matching_consulta.idreporte_id).first()
    matching_result_info = FetoMedicionDiagnostico.objects.filter(reporte=matching_report.idreporte)
    
    return matching_consulta, matching_patient, matching_clinichist, matching_report, matching_result_info


def get_mediciones():
    return  {'hc_hadlock': 1, 'bpd_hadlock': 2, 'cereb_hill': 3, 'efw':4, 'csp':5, 'cm':5, 'vp':6, 'va':7, 'afi':8}

