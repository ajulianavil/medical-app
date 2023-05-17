from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from users.context_processors import current_user
from main.models import *

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        # fields = ['email','first_name', 'last_name', 'username',  'password1', 'password2', 'is_staff']
        # fields = '__all__' 
        fields = ['email', 'roles', 'description', 'username',]

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
    
class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class PersonalsaludForm(forms.ModelForm):
    dropdown_field = forms.ModelChoiceField(queryset=Hospital.objects.all())
    
    nombres = forms.CharField(label="Nombres", max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}) )
    apellidos = forms.CharField(label="Apellidos", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}) )
    identificacion = forms.IntegerField(label="Número de identificación", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}) )
    telefono = forms.CharField(label="Teléfono", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}) )
    direccion = forms.CharField(label="Dirección de residencia", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}) )
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), label="Hospital en el que labora", required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    userid = 2
    
    print("USER ID", userid)
    
    def save(self, commit=True):
        user_data = super().save(commit=False)
        user_data.nombresmed = self.cleaned_data['nombres']
        user_data.apellidosmed = self.cleaned_data['apellidos']
        user_data.cedulamed = self.cleaned_data['identificacion']
        user_data.telefonomed = self.cleaned_data['telefono']
        user_data.direccionmed = self.cleaned_data['direccion']
        user_data.userid = self.cleaned_data['userid']
        user_data.hospital = self.cleaned_data['hospital']

        if commit:
            user_data.save()
        return user_data

    class Meta:
        model = Personalsalud
        fields = '__all__'