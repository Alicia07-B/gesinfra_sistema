# fix_all_problems.py
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gesinfra_sistema.settings')
django.setup()

from django.template.loader import render_to_string
from django.conf import settings

print("=" * 80)
print("SOLUCIÓN COMPLETA DE BOTONES Y FORMULARIOS")
print("=" * 80)

# 1. Crear todas las plantillas necesarias
print("\n📝 1. CREANDO PLANTILLAS COMPLETAS...")

plantillas = {
    # Plantillas de Calificaciones
    'calificaciones/templates/calificaciones/base.html': '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Gesinfra Web{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #2c3e50;
            --secondary: #3498db;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --info: #17a2b8;
        }
        .sidebar {
            background: linear-gradient(180deg, var(--primary) 0%, #1a252f 100%);
            color: white;
            min-height: 100vh;
        }
        .nav-link {
            color: rgba(255,255,255,0.8);
            padding: 12px 20px;
            border-left: 4px solid transparent;
        }
        .nav-link:hover, .nav-link.active {
            background: rgba(255,255,255,0.1);
            color: white;
            border-left: 4px solid var(--secondary);
        }
        .module-badge {
            background: var(--secondary);
            color: white;
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    {% if user.is_authenticated %}
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <nav class="col-md-3 col-lg-2 d-md-block sidebar">
                <div class="position-sticky pt-3">
                    <div class="text-center p-3">
                        <h5><i class="fas fa-school me-2"></i>GesInfra Web</h5>
                        <small class="text-muted">Sistema Integral</small>
                    </div>
                    
                    <ul class="nav flex-column">
                        <!-- Dashboard -->
                        <li class="nav-item">
                            <a class="nav-link {% if request.path == '/' %}active{% endif %}" href="/">
                                <i class="fas fa-tachometer-alt me-2"></i>Dashboard
                            </a>
                        </li>
                        
                        <!-- MÓDULO CALIFICACIONES -->
                        <li class="nav-item mt-3">
                            <small class="text-light ms-3"><i class="fas fa-graduation-cap me-1"></i>CALIFICACIONES</small>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {% if 'calificaciones/estudiantes' in request.path %}active{% endif %}" 
                               href="{% url 'calificaciones:lista_estudiantes' %}">
                                <i class="fas fa-users me-2"></i>Estudiantes
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {% if 'calificaciones/docentes' in request.path %}active{% endif %}" 
                               href="{% url 'calificaciones:lista_docentes' %}">
                                <i class="fas fa-chalkboard-teacher me-2"></i>Docentes
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {% if 'calificaciones/asignaturas' in request.path %}active{% endif %}" 
                               href="{% url 'calificaciones:lista_asignaturas %}">
                                <i class="fas fa-book me-2"></i>Asignaturas
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {% if 'calificaciones/calificaciones' in request.path %}active{% endif %}" 
                               href="{% url 'calificaciones:lista_calificaciones %}">
                                <i class="fas fa-graduation-cap me-2"></i>Calificaciones
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {% if 'calificaciones/reportes' in request.path %}active{% endif %}" 
                               href="{% url 'calificaciones:reportes %}">
                                <i class="fas fa-file-pdf me-2"></i>Reportes
                            </a>
                        </li>
                        
                        <!-- Otros módulos... -->
                    </ul>
                </div>
            </nav>
            
            <!-- Main content -->
            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                {% block content %}{% endblock %}
            </main>
        </div>
    </div>
    {% endif %}
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>''',

    # Login template
    'registration/login.html': '''{% extends 'base.html' %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0"><i class="fas fa-sign-in-alt me-2"></i>Iniciar Sesión</h4>
                </div>
                <div class="card-body">
                    {% if form.errors %}
                    <div class="alert alert-danger">
                        Usuario o contraseña incorrectos.
                    </div>
                    {% endif %}
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="mb-3">
                            <label for="username" class="form-label">Usuario</label>
                            <input type="text" name="username" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Contraseña</label>
                            <input type="password" name="password" class="form-control" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">
                            <i class="fas fa-sign-in-alt me-2"></i>Ingresar
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
}

# Crear directorios y archivos
for ruta, contenido in plantillas.items():
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"✓ {ruta} creada")
    except Exception as e:
        print(f"✗ Error creando {ruta}: {e}")

# 2. Verificar y crear URLs faltantes
print("\n🔗 2. VERIFICANDO URLS...")

from django.urls import reverse, NoReverseMatch
from calificaciones import urls as calificaciones_urls

# Lista de URLs que deben existir
urls_requeridas = [
    'calificaciones:lista_estudiantes',
    'calificaciones:agregar_estudiante',
    'calificaciones:editar_estudiante',
    'calificaciones:eliminar_estudiante',
    'calificaciones:lista_docentes',
    'calificaciones:agregar_docente',
    'calificaciones:lista_asignaturas',
    'calificaciones:agregar_asignatura',
    'calificaciones:lista_calificaciones',
    'calificaciones:agregar_calificacion',
    'calificaciones:editar_calificacion',
    'calificaciones:reportes',
    'calificaciones:boleta_calificaciones',
    'calificaciones:generar_reporte_individual_pdf',
    'login',
    'logout',
]

print("\nURLs disponibles:")
for url_name in urls_requeridas:
    try:
        url = reverse(url_name)
        print(f"✓ {url_name}: {url}")
    except NoReverseMatch:
        print(f"✗ {url_name}: NO EXISTE")

# 3. Crear archivo de URLs completo
print("\n📋 3. CREANDO ARCHIVO DE URLS COMPLETO...")

urls_content = '''# calificaciones/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'calificaciones'

urlpatterns = [
    # Dashboard y principal
    path('', views.dashboard, name='dashboard'),
    
    # Estudiantes
    path('estudiantes/', views.lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/agregar/', views.agregar_estudiante, name='agregar_estudiante'),
    path('estudiantes/editar/<int:id>/', views.editar_estudiante, name='editar_estudiante'),
    path('estudiantes/eliminar/<int:id>/', views.eliminar_estudiante, name='eliminar_estudiante'),
    
    # Docentes
    path('docentes/', views.lista_docentes, name='lista_docentes'),
    path('docentes/agregar/', views.agregar_docente, name='agregar_docente'),
    path('docentes/editar/<int:id>/', views.editar_docente, name='editar_docente'),
    
    # Asignaturas
    path('asignaturas/', views.lista_asignaturas, name='lista_asignaturas'),
    path('asignaturas/agregar/', views.agregar_asignatura, name='agregar_asignatura'),
    path('asignaturas/editar/<int:id>/', views.editar_asignatura, name='editar_asignatura'),
    
    # Calificaciones
    path('calificaciones/', views.lista_calificaciones, name='lista_calificaciones'),
    path('calificaciones/agregar/', views.agregar_calificacion, name='agregar_calificacion'),
    path('calificaciones/editar/<int:id>/', views.editar_calificacion, name='editar_calificacion'),
    path('calificaciones/gestionar/', views.gestionar_calificaciones, name='gestionar_calificaciones'),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/boleta/', views.boleta_calificaciones, name='boleta_calificaciones'),
    path('reportes/individual/<int:estudiante_id>/pdf/', 
         views.generar_reporte_individual_pdf, name='generar_reporte_individual_pdf'),
    
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
'''

try:
    with open('calificaciones/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    print("✓ calificaciones/urls.py actualizado")
except Exception as e:
    print(f"✗ Error: {e}")

# 4. Verificar vistas
print("\n👁️  4. VERIFICANDO VISTAS...")

from django.apps import apps

try:
    from calificaciones import views
    vistas_requeridas = [
        'dashboard',
        'lista_estudiantes', 'agregar_estudiante', 'editar_estudiante', 'eliminar_estudiante',
        'lista_docentes', 'agregar_docente', 'editar_docente',
        'lista_asignaturas', 'agregar_asignatura', 'editar_asignatura',
        'lista_calificaciones', 'agregar_calificacion', 'editar_calificacion',
        'gestionar_calificaciones', 'reportes', 'boleta_calificaciones',
        'generar_reporte_individual_pdf'
    ]
    
    print("\nVistas encontradas:")
    for vista in vistas_requeridas:
        if hasattr(views, vista):
            print(f"✓ {vista}")
        else:
            print(f"✗ {vista} - FALTA")
except Exception as e:
    print(f"✗ Error verificando vistas: {e}")

print("\n" + "=" * 80)
print("✅ PROCESO COMPLETADO")
print("=" * 80)
print("\n📋 PASOS SIGUIENTES:")
print("1. Ejecuta: python manage.py runserver")
print("2. Accede a: http://localhost:8000/")
print("3. Usuario: admin (o el que hayas creado)")
print("\n🔧 Si hay errores, ejecuta:")
print("   python manage.py makemigrations")
print("   python manage.py migrate")
