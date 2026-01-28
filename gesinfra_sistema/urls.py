# gesinfra_sistema/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from usuarios.views import dashboard as usuarios_dashboard
from django.contrib.auth import views as auth_views


def redirect_to_dashboard(request):
    return redirect('calificaciones:dashboard')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/usuarios/dashboard/')),  # Redirige al dashboard de usuarios
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('inventario/', include('inventario.urls')),
    path('calificaciones/', include('calificaciones.urls')),
    path('accesibilidad/', include('accesibilidad.urls')),
    path('calificaciones/', include('calificaciones.urls')),

    path('', auth_views.LoginView.as_view(template_name='calificaciones/auth/login.html'), name='login'),
    path('', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('', auth_views.LoginView.as_view(
        template_name='calificaciones/auth/login.html'), name='home'),
]