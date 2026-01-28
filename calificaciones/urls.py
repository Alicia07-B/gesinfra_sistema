# calificaciones/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

app_name = 'calificaciones'  # <-- DEFINIR AQUÍ el namespace
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('estudiantes/', views.ListaEstudiantesView.as_view(), name='lista_estudiantes'),
    path('estudiantes/agregar/', views.agregar_estudiante, name='agregar_estudiante'),
    path('estudiantes/editar/<int:id>/', views.editar_estudiante, name='editar_estudiante'),
    path('estudiantes/eliminar/<int:id>/', views.eliminar_estudiante, name='eliminar_estudiante'),
    
    path('docentes/', views.lista_docentes, name='lista_docentes'),
    path('docentes/agregar/', views.agregar_docente, name='agregar_docente'),
    path('docentes/editar/<int:id>/', views.editar_docente, name='editar_docente'),
    
    path('asignaturas/', views.lista_asignaturas, name='lista_asignaturas'),
    path('asignaturas/agregar/', views.agregar_asignatura, name='agregar_asignatura'),
    path('asignaturas/editar/<int:id>/', views.editar_asignatura, name='editar_asignatura'),
    
    path('periodos/', views.lista_periodos, name='lista_periodos'),
    
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/agregar/', views.agregar_curso, name='agregar_curso'),
    path('cursos/editar/<int:id>/', views.editar_curso, name='editar_curso'),
    path('cursos/eliminar/<int:id>/', views.eliminar_curso, name='eliminar_curso'),
    
    path('matriculas/', views.lista_matriculas, name='lista_matriculas'),
    path('matriculas/agregar/', views.agregar_matricula, name='agregar_matricula'),
    path('matriculas/editar/<int:id>/', views.editar_matricula, name='editar_matricula'),
    path('matriculas/eliminar/<int:id>/', views.eliminar_matricula, name='eliminar_matricula'),
    
    path('configuracion/<int:asignatura_id>/', views.configuracion_evaluacion, name='configuracion_evaluacion'),
    path('configuracion/eliminar/<int:config_id>/', views.eliminar_configuracion, name='eliminar_configuracion'),
    
    path('calificaciones/', views.lista_calificaciones, name='lista_calificaciones'),
    path('calificaciones/agregar/', views.agregar_calificacion, name='agregar_calificacion'),
    path('calificaciones/editar/<int:id>/', views.editar_calificacion, name='editar_calificacion'),
    path('calificaciones/gestionar/', views.gestionar_calificaciones, name='gestionar_calificaciones'),
    path('api/calificacion/', views.get_calificacion_estudiante, name='get_calificacion'),
    
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/boleta/', views.boleta_calificaciones, name='boleta_calificaciones'),
    path('reportes/pdf/<int:estudiante_id>/', views.generar_reporte_individual_pdf, name='reporte_pdf'),
    path('reportes/pdf/grupo/', views.generar_reporte_grupo_pdf, name='reporte_grupal_pdf'),
    
    path('registro/', views.registro_docente, name='registro_docente'),
    
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    
    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='calificaciones:login'
    ), name='logout'),
]
