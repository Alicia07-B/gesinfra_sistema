# calificaciones/admin.py - SOLO CLASES ADMIN, NO MODELOS
from django.contrib import admin
from .models import *

# ========== ADMIN PARA ESTUDIANTES ==========
@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre_completo', 'cedula', 'email', 'activo']
    list_filter = ['activo', 'genero']
    search_fields = ['codigo', 'nombre', 'apellido', 'cedula']
    ordering = ['apellido', 'nombre']

# ========== ADMIN PARA DOCENTES ==========
@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre_completo', 'cedula', 'especialidad', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre', 'apellido']
    ordering = ['apellido', 'nombre']

# ========== ADMIN PARA ASIGNATURAS ==========
@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre','horas_semana', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
    ordering = ['codigo']

# ========== ADMIN PARA PERIODOS ==========
@admin.register(PeriodoAcademico)
class PeriodoAcademicoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_inicio', 'fecha_fin', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']
    ordering = ['-fecha_inicio']

# ========== ADMIN PARA CURSOS ==========
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'asignatura', 'periodo', 'seccion', 'docente', 'cupo_actual', 'cupo_maximo', 'activo']
    list_filter = ['activo', 'periodo', 'asignatura']
    search_fields = ['codigo', 'seccion']
    list_select_related = ['asignatura', 'periodo', 'docente']

# ========== ADMIN PARA MATRÍCULAS ==========
@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['id_matricula', 'estudiante', 'curso', 'fecha_matricula', 'estado', 'nota_final']
    list_filter = ['estado', 'fecha_matricula']
    search_fields = ['estudiante__nombre', 'estudiante__apellido', 'curso__codigo']
    list_select_related = ['estudiante', 'curso']

# ========== ADMIN PARA CONFIGURACIÓN EVALUACIÓN ==========
@admin.register(ConfiguracionEvaluacion)
class ConfiguracionEvaluacionAdmin(admin.ModelAdmin):
    list_display = ['nombre_evaluacion', 'asignatura', 'porcentaje', 'activo']
    list_filter = ['activo', 'asignatura']
    search_fields = ['nombre_evaluacion', 'asignatura__nombre']
    ordering = ['asignatura', 'porcentaje']

# ========== ADMIN PARA CALIFICACIONES ==========
@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['id_calificacion', 'matricula', 'configuracion', 'nota', 'nota_ponderada', 'fecha_registro']
    list_filter = ['configuracion', 'fecha_registro']
    search_fields = ['matricula__estudiante__nombre', 'matricula__estudiante__apellido']
    list_select_related = ['matricula', 'configuracion']
