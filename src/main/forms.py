from django import forms
from users.models import Appuser
from django.contrib.auth.hashers import make_password


class UploadFileForm(forms.Form):
    file = forms.FileField()


class CreateUserForm(forms.ModelForm):
    email = forms.EmailField(label="Correo electrónico",max_length=50, required=True, widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}) )
    password = forms.CharField(label="Contraseña",required=True, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Contraseña'}) )
    repassword = forms.CharField(label="Repetir contraseña", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Repetir contraseña'}) )
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('repassword')

        if password1 and password2 and password1 != password2:
            self.add_error("repassword","Passwords do not match")
            raise forms.ValidationError('Passwords do not match')

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = Appuser
        fields = ['email', 'password', 'roles']