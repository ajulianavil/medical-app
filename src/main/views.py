from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
# Create your views here.
def landing(request):
    return render(request, 'main/landing.html')

def aboutUs(request):
    return render(request, 'main/aboutUs.html')

def howToRegister(request):
    return render(request, 'main/howToRegister.html')

def homepage(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    current_user = request.user
    user = get_user_model().objects.filter(email=current_user).first()
    return render(request, 'main/home.html', {'user': user})
   