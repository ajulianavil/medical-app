from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, 'main/landing.html')

def aboutUs(request):
    return render(request, 'main/aboutUs.html')


