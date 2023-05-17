from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from main.models import Personalsalud
from users.context_processors import current_user
from users.models import *
from .forms import PersonalsaludForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import ContactForm


def contact(request):
    form = ContactForm()
    return render(request, 'users/contact.html', {'form': form})

# Create your views here.
def register(request):
    # if request.user.is_authenticated:
        # return redirect('/')

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"New account created: {user.username}")
            return redirect('/')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="users/register.html",
        context={"form": form}
        )

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/login')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect('/')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 

    form = AuthenticationForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={"form": form}
        )
    
def profile(request):
    if request.user.is_authenticated:
        user_logged = current_user(request)
        info = list(user_logged.values())

        user_info = {
        'user_email': info[0]['useremail'],
        'user_id': info[0]['userid'],
        'user_name': info[0]['user_name'],
        'user_lastname': info[0]['user_lastname'],
        'user_identification': info[0]['user_identification'],
        'user_phone': info[0]['user_phone'],
        'user_address': info[0]['user_address'],
        'user_password': info[0]['userpassword'],
        'user_role': 'Médico' if info[0]['userrol'] == 'médico' else 'Investigador'
        }

    return render(request, 'users/profile.html', context= {"user_info":user_info})

def user_data(request):
    user_logged = request.user  # Replace 'function' with the actual attribute or related model
    print("PRIMERO")
    if request.method == "POST":
        print("ES POST")
        form = PersonalsaludForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("VALIDO")
            form.save()
            messages.success(request, 'El registro ha sido finalizado con éxito')
            rol = Appuser.objects.filter(email=user_logged).first()
            # rol = request.GET.get('rol')
            form = PersonalsaludForm()
            return render(request, 'consultas/agregar_consulta.html', {"form": form, "rol": rol,})
        else:
            print("NO VALIDO")
            messages.error(request, 'Hay un problema con el formulario.')
            rol = request.GET.get('rol')
            return render(request, 'users/user_data.html', {"form": form, "rol": rol})
        
    else:
        print("NO ES POST")
        rol = Appuser.objects.filter(email=user_logged).first()
        
        if rol:
            form = PersonalsaludForm()
            return render(request, 'users/user_data.html', {"form": form, "rol": rol})
        
        if not request.user.is_authenticated:
            return redirect('/login')   
        return render(request, 'users/user_data.html')
    # , {'form': form}
    return render(request, 'users/user_data.html', {'form': form})