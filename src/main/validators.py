from django import forms
from django.core.exceptions import ValidationError

def val_cedulamed(cedulamed):
    if len(str(cedulamed)) < 4:
        raise ValidationError("El número de identificación debe sere mayor a 4 digitos") 
    if len(str(cedulamed)) > 10:
        raise ValidationError("El número de identificación no puede exceder los 10 dígitos") 
    
def val_cedulaext(cedulaext):
    if len(str(cedulaext)) < 4:
        raise ValidationError("El número de identificación debe sere mayor a 4 digitos") 
    if len(str(cedulaext)) > 10:
        raise ValidationError("El número de identificación no puede exceder los 10 dígitos") 

def val_cedulapac(cedulapac):
    if len(str(cedulapac)) < 4:
        raise ValidationError("El número de identificación debe sere mayor a 4 digitos") 
    if len(str(cedulapac)) > 10:
        raise ValidationError("El número de identificación no puede exceder los 10 dígitos") 
