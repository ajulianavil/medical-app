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
    
    nombresmed = forms.CharField(label="Nombres", max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}) )
    apellidosmed = forms.CharField(label="Apellidos", max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}) )
    cedulamed = forms.IntegerField(label="Número de identificación", required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' '}) )
    telefonomed = forms.CharField(label="Teléfono",required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' ', 'inputmode': 'numeric'}) )
    direccionmed = forms.CharField(label="Dirección de residencia", max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}) )
    hospitalid = forms.ModelChoiceField(queryset=Hospital.objects.all(), label="Hospital en el que labora", required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombresmed = self.cleaned_data['nombresmed']
        user.apellidosmed = self.cleaned_data['apellidosmed']
        user.cedulamed = self.cleaned_data['cedulamed']
        user.telefonomed = self.cleaned_data['telefonomed']
        user.direccionmed = self.cleaned_data['direccionmed']
        user.hospitalid = self.cleaned_data['hospitalid']
        if commit:
            user.save()
        return user

    class Meta:
        model = Personalsalud
        fields = ['nombresmed', 'apellidosmed', 'cedulamed', 'telefonomed', 'direccionmed', 'hospitalid']