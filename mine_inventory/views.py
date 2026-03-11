from django.shortcuts import render

# Create your views here.
def home(request):
    nombre = 'Felipe'
    context = {
        'nombre': nombre,
        'titulo': 'Home'
    }
    return render(request, 'home.html', context)