from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from calificaciones.models import Estudiante, Calificacion, Docente

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('usuarios:login')
@login_required
def dashboard(request):
    # Redirige al dashboard principal de calificaciones
    return redirect('calificaciones:dashboard')

@login_required
def dashboard(request):
    # Importar aquí para evitar circular imports
    try:
        estudiantes_count = Estudiante.objects.count()
        calificaciones_count = Calificacion.objects.count()
        docentes_count = Docente.objects.count()
    except:
        # Si las tablas no existen aún
        estudiantes_count = 0
        calificaciones_count = 0
        docentes_count = 0
    
    context = {
        'estudiantes_count': estudiantes_count,
        'calificaciones_count': calificaciones_count,
        'docentes_count': docentes_count,
    }
    return render(request, 'usuarios/dashboard.html', context)