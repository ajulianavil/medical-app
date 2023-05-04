import numpy as np

from main.models import Medicion, Tipomedicion

def process_data(file):
    file_readed = file.readlines()
    count = 0
    for row_bytes in file_readed:
        row = row_bytes.decode("utf-8") 
        print('=========')
        if ('STUDYDATE' in row):
            studydate = row.strip().split(" ")[1]
        elif ('STUDYTIME' in row):
            studytime = row.strip().split(" ")[1]
        elif ('HOSPITAL' in row):
            hospital = row.strip().split(" ")[1]
            hospital = hospital[1:]
            hospital = hospital[:-1]
        elif ('PERFORMING_PH' in row):
            med_name = row.strip().split(" ")[1]
            med_name = med_name[1:]
            med_lastname = row.strip().split(" ")[2]
            med_lastname = med_lastname[:-1]
        elif ('PATNAME' in row):
            pat_fullname = row.strip().split(" ")[1]
            pat_fullname = row.strip().split(", ")
            pat_name = pat_fullname[1][:-1]
            pat_lastname = pat_fullname[0].split(" ")[1][1:]
        elif ('PATID' in row):
            pat_id = row.strip().split(" ")[1]
            pat_id = pat_id[1:]
            pat_id = pat_id[:-1]
        elif ('GESTATIONS' in row):
            num_gesta = row.strip().split(" ")[1]
        elif ('CLINICAL_LMP' in row):
            clinical_lmp = row.strip().split(" ")[1]
        elif ('CLINICAL_GA' in row):
            clinical_ga = row.strip().split(" ")
            ga_weeks = clinical_ga[1][:-1]
            ga_days = clinical_ga[2][:-1]
            clinical_ga = ga_weeks+" "+ga_days
        elif ('CLINICAL_EDC' in row):
            CLINICAL_EDC = row.strip().split(" ")[1]
        elif ('EFW_HADLOCK' in row):
            EFW = row.strip().split(" ")[1] # Estimated Fetal Weight
    count += 1
    #texto = "El día", STUDYDATE, "a las", STUDYTIME, "se realiza una ecografía a la paciente con número de cédula", PAT_ID, ". La paciente presentó su último periodo menstrual (LMP) el día", CLINICAL_LMP, "por lo que la edad gestacional del feto calculada a partir de dicha fecha es de", GA_weeks_numberOnly, "semanas", GA_days_numberOnly, "días y su fecha estimada de parto está para", CLINICAL_EDC, ". El feto tiene un peso estimado de ", EFW, "gramos."
    convertedDate = ConvertDateTime(studydate, studytime)
    insert_paciente = {
    'cedulapac': pat_id,
    'apellido_paterno': pat_lastname,
    'nombreuno':pat_name,
    'numgestacion':num_gesta
    }
    
    count = 0
    for row_bytes in file_readed:
        line = row_bytes.decode("utf-8") 
    # BIORBITAL DIAMETER Diámetro bi-orbitario externo
        if ('BOD_JEANTY' in line):
            BOD_JEANTY = line.strip().split("|")
            BOD_JEANTY = BOD_JEANTY[:-1]
            BOD_JEANTY = BOD_JEANTY[0].split("=")[1].split(" ")[0] #1
            BOD_JEANTY = (float(BOD_JEANTY)*10) #To mm
        # diámetro transverso del cerebelo
        if ('CEREB_HILL' in line):
            CEREB_HILL = line.strip().split("|")
            CEREB_HILL = CEREB_HILL[:-1]
            cereb_hill_1 = CEREB_HILL[0].split("=")[1].split(" ")[0] #1
            cereb_hill_1 = np.round((float(cereb_hill_1)*10), decimals=2) #To mm
            cereb_hill_avg = CEREB_HILL[1].split("=")[1].split(" ")[0] #1
            cereb_hill_avg = np.round((float(cereb_hill_avg)*10), decimals=2) #To mm
            cereb_hill_ga_weeks  = CEREB_HILL[2].split("=")[1].split(" ")[0]
            cereb_hill_ga_days = CEREB_HILL[2].split("=")[1].split(" ")[1]
            cereb_hill_ga  = cereb_hill_ga_weeks+" "+cereb_hill_ga_days                
            cereb_hill_edc = CEREB_HILL[3].split("=")[1].split(" ")[0] #1
            cereb_hill_dev = CEREB_HILL[4].split("=")[1].split(" ")[0][:-1] #1
        # BIPARIETAL DIAMETER Diametro Biparietal (Distancia en milímetros entre ambos huesos parietales de la cabeza del bebé)
        if ('BPD_HADLOCK' in line):
            BPD_HADLOCK = line.strip().split("|")
            BPD_HADLOCK = BPD_HADLOCK[:-1]
            bpd_hadlock_1 = BPD_HADLOCK[0].split("=")[1].split(" ")[0] #1
            bpd_hadlock_1 = np.round((float(bpd_hadlock_1)*10), decimals=2) #To mm
            bpd_hadlock_avg = BPD_HADLOCK[1].split("=")[1].split(" ")[0] #1
            bpd_hadlock_avg = np.round((float(bpd_hadlock_avg)*10), decimals=2) #To mm
            bpd_hadlock_ga_weeks  = BPD_HADLOCK[2].split("=")[1].split(" ")[0] 
            bpd_hadlock_ga_days = BPD_HADLOCK[2].split("=")[1].split(" ")[1] 
            bpd_hadlock_ga  = bpd_hadlock_ga_weeks+" "+bpd_hadlock_ga_days                
            bpd_hadlock_edc = BPD_HADLOCK[3].split("=")[1].split(" ")[0] #1
            bpd_hadlock_dev = BPD_HADLOCK[4].split("=")[1].split(" ")[0][:-1] #1
        # CISTERNA MAGNA
        if ('CM' in line):
            CM = line.strip().split("|")
            CM = CM[:-1]
            cm_1 = CM[0].split("=")[1].split(" ")[0] #1
            cm_avg = CM[1].split("=")[1].split(" ")[0] #1
        # CAVUM SEPTI PELLUCIDI
        if ('CSP' in line):
            CSP = line.strip().split("|")
            CSP = CSP[:-1]
            csp_1 = CSP[0].split("=")[1].split(" ")[0] #1
            csp_avg = CSP[1].split("=")[1].split(" ")[0] #2
        # HEAD CIRCUMFERENCE
        if ('HC_HADLOCK' in line):
            HC_HADLOCK = line.strip().split("|")
            HC_HADLOCK = HC_HADLOCK[:-1]
            hc_hadlock_1 = HC_HADLOCK[0].split("=")[1].split(" ")[0] #1
            hc_hadlock_avg = HC_HADLOCK[1].split("=")[1].split(" ")[0] 
            hc_hadlock_ga_weeks  = HC_HADLOCK[2].split("=")[1].split(" ")[0] 
            hc_hadlock_ga_days = HC_HADLOCK[2].split("=")[1].split(" ")[1] 
            hc_hadlock_ga  = hc_hadlock_ga_weeks+" "+hc_hadlock_ga_days
            hc_hadlock_edc = HC_HADLOCK[3].split("=")[1].split(" ")[0] 
            hc_hadlock_dev = HC_HADLOCK[4].split("=")[1].split(" ")[0][:-1] 
            hc_hadlock_1 = np.round((float(hc_hadlock_1)*10), decimals=2) #To mm
            hc_hadlock_avg = np.round((float(hc_hadlock_avg)*10), decimals=2) #To mm
        # Va Anterior Ventricle
        if ('Va' in line):
            Va = line.strip().split("|")
            Va = Va[:-1]
            va_1= Va[0].split("=")[1].split(" ")[0] #1
            va_avg = Va[0].split("=")[1].split(" ")[0] #1
        # Vp Posterior ventricle
        if ('Vp' in line):
            Vp = line.strip().split("|")
            Vp = Vp[:-1]
            vp_1 = Vp[0].split("=")[1].split(" ")[0] #1
            vp_avg = Vp[0].split("=")[1].split(" ")[0] #1
        if ('AFI' in line):
            afi = line.strip().split("|")
            afi = afi[:-1]
            afi_sum = afi[4].split("=")[1].split(" ")[0]
            
    textodos = "El Vp es de", Vp
    reporte_info = {
        'efw': EFW,
        'edb': CLINICAL_EDC,
        'ga': ga_weeks,
        'csp_1': csp_1,
        'csp_avg': csp_avg,
        'cm_1': cm_1,
        'cm_avg': cm_avg,
        'hc_hadlock_1': hc_hadlock_1,
        'hc_hadlock_avg': hc_hadlock_avg,
        'hc_hadlock_ga': hc_hadlock_ga,
        'hc_hadlock_edc': hc_hadlock_edc,
        'hc_hadlock_dev': hc_hadlock_dev,
        'bdp_hadlock_1': bpd_hadlock_1,
        'bdp_hadlock_avg': bpd_hadlock_avg,
        'bdp_hadlock_ga': bpd_hadlock_ga,
        'bdp_hadlock_edc': bpd_hadlock_edc,
        'bdp_hadlock_dev': bpd_hadlock_dev,
        'cereb_hill_1': cereb_hill_1,
        'cereb_hill_avg': cereb_hill_avg,
        'cereb_hill_ga': cereb_hill_ga,
        'cereb_hill_edc': cereb_hill_edc,
        'cereb_hill_dev': cereb_hill_dev,
        'va_1': va_1,
        'va_avg': va_avg,
        'vp_1': vp_1,
        'vp_avg': vp_avg,
        'ga_days': ga_days,
        'afi': afi_sum
    }
    
    return insert_paciente, reporte_info, convertedDate, clinical_lmp, med_name, med_lastname

    
def ConvertDateTime(studydate, studytime):
    day = studydate.split(".")[0]
    month = studydate.split(".")[1]
    year = studydate.split(".")[2]
    
    fullDate = year+"-"+month+"-"+day+" "+studytime
    return fullDate

def comparison(diagnosisData):
    gest_age = diagnosisData['ga']
    
    #'nombreMedicion': valorDatoReporte
    valores_normales = {}
    #'nombreMedicion': [Diagnostico, valorDatoReporte, valorReferencia]
    valores_anormales = {}
    
    data = {'hc_hadlock': diagnosisData['hc_hadlock_1'], 'bpd_hadlock': diagnosisData['bdp_hadlock_1'], 'csp': diagnosisData['hc_hadlock_1'],
            'cm': diagnosisData['cm_1'], 'vp': diagnosisData['vp_1'], 'va': diagnosisData['va_1'], 'cereb_hill': diagnosisData['cereb_hill_1'],
            'efw': diagnosisData['efw'], 'afi': diagnosisData['afi']}

    # print("DATOS", data)
    tipos_mediciones = Tipomedicion.objects.all()
    mediciones = {}
    
    # Guarda el id y el nombre de cada tipo de medición
    for obj in tipos_mediciones:
        mediciones[obj.idTipoMedicion] = obj.nombreMedicion

    #Filtra por tipo de medicion y luego por edad gestional
    # valorinter -> valor max || valordev -> valordev(valor intermedio)
    for key in mediciones:
        #or key == 7
        if key == 1 or key == 2 or key == 7:
            try:
                med = Medicion.objects.get(id_tipo_medicion=key, ga=gest_age)
                
                if key == 1: #HC_HADLOCK
                    if (data["hc_hadlock"] > med.valorinter):
                        
                        valores_anormales.update({'Circunferencia de la cabeza (HC_HADLOCK)': ['Macro', data["hc_hadlock"], med.valorinter]})
                        print("Macroo")
                        
                    elif (data["hc_hadlock"] < med.valormin):
                        valores_anormales.update({'Circunferencia de la cabeza (HC_HADLOCK)': ['Microcefalia', data["hc_hadlock"], med.valormin]})
                        print("Microcefalia")
                    else:
                        valores_normales.update({'Circunferencia de la cabeza (HC_HADLOCK)': data["hc_hadlock"]})
                        print("OK - HC en valores normales")

                if key == 2: #BPD
                    if (data["bpd_hadlock"] > med.valorinter):
                        valores_anormales.update({'Diámetro biparietal (BPD_HADLOCK)': ['Valor superior al normal', data["bpd_hadlock"], med.valorinter]})
                        print("bpd_hadlock valor superior al normal")
                        
                    elif (data["bpd_hadlock"] < med.valormin):
                        valores_anormales.update({'Diámetro biparietal (BPD_HADLOCK)': ['Valor inferior al normal', data["bpd_hadlock"], med.valormin]})
                        print("bpd_hadlock valor inferior al normal")
                        
                    else:
                        valores_normales.update({'Diámetro biparietal (BPD_HADLOCK)': data["bpd_hadlock"]})
                        print("OK - bpd_hadlock valores normales")
                        
                if key == 7: #Diametro transverso del cerebelo CEREB_HILL
                    print("cerebhill")
                    # if (data["cereb_hill"] < med.valormin):
                    #     print("Hipoplasia cereberal")
                    # else:
                    #     print("OK - cereb_hill en valores normales")
                                
            except Medicion.DoesNotExist:
                med = None
                print("Para la llave:", key, "no se encontró nada con esta edad gestacional")
                     
        if key == 3: #CSP
            print("CSP")
        
        if key == 4: #CM -> Para todas las edades
            if (float(data["cm"]) > 10):
                valores_anormales.update({'Cisterna Magna (CM)': ['Megacisterno o cisterno alargada', data["cm"], 10]})
                print("Megacisterno o cisterno alargada")
            else:
                valores_normales.update({'Cisterna Magna (CM)': data["cm"]})
                print("OK - CM en valores normales")
        
        if key == 5 or key == 6: #VP or VA
            if (float(data["vp"]) < 9.9 or float(data["va"]) < 9.9):
                valores_normales.update({'Ventrículo posterior': data["vp"]})
                valores_normales.update({'Ventrículo anterior': data["va"]})
                print("Normal")
                
            elif ((10 < float(data["vp"]) < 11.9) or (10 < float(data["va"]) < 11.9)):
                valores_anormales.update({'Ventrículo posterior (VP)': ['Ventriculomegalia leve', data["vp"], '10 - 11.9']})
                valores_anormales.update({'Ventrículo anterior (VA)': ['Ventriculomegalia leve', data["va"], '10 - 11.9']})
                print("Ventriculomegalia leve")
                
            elif ((12 < float(data["vp"]) < 14.9) or (12 < float(data["va"]) < 14.9)):
                valores_anormales.update({'Ventrículo posterior (VP)': ['Ventriculomegalia moderada', data["vp"], '12 - 14.9']})
                valores_anormales.update({'Ventrículo anterior (VA)': ['Ventriculomegalia moderada', data["va"], '12 - 14.9']})
                print("Ventriculomegalia moderada")   
                
            elif (float(data["vp"]) > 15 or float(data["va"]) > 15):
                valores_anormales.update({'Ventrículo posterior (VP)': ['Ventriculomegalia severa', data["vp"], 15]})
                valores_anormales.update({'Ventrículo anterior (VA)': ['Ventriculomegalia severa', data["va"], 15]})
                print("Ventriculomegalia severa")
                
            else:
                valores_normales.update({'Ventrículo posterior': data["vp"]})
                valores_normales.update({'Ventrículo anterior': data["va"]})
                print("OK - VP y VA en valores normales")
                
        # if key == 6: #VA
        #     print("VA")
        if key == 8:
            if (float(data["afi"]) < 5):
                valores_anormales.update({'Indice de líquido amniótico (AFI)': ['Oligohidramnios', data["afi"], 5]})
                print("Oligohidramnios")
                
            elif (5 < float(data["afi"]) < 24):
                valores_normales.update({'Indice de líquido amniótico (AFI)': data["afi"]})
                print("AFI Normal")
                
            elif (float(data["afi"]) > 24):
                valores_anormales.update({'Indice de líquido amniótico (AFI)': ['Polihidramnios', data["afi"], 24]})
                print("Polihidramnios")
                
                
                
    
        
    