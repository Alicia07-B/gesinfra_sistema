# calificaciones/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Sum, Avg, Count
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import json
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *

# ========== DASHBOARD ==========

@login_required
def dashboard(request):
    """Dashboard principal"""
    # Estadísticas
    total_estudiantes = Estudiante.objects.filter(activo=True).count()
    total_docentes = Docente.objects.filter(activo=True).count()
    total_asignaturas = Asignatura.objects.filter(activo=True).count()
    total_matriculas = Matricula.objects.count()
    
    # Últimos estudiantes registrados
    ultimos_estudiantes = Estudiante.objects.order_by('-fecha_registro')[:5]
    
    # Período activo
    periodo_actual = PeriodoAcademico.objects.filter(activo=True).first()
    
    context = {
        'titulo': 'Dashboard',
        'total_estudiantes': total_estudiantes,
        'total_docentes': total_docentes,
        'total_asignaturas': total_asignaturas,
        'total_matriculas': total_matriculas,
        'ultimos_estudiantes': ultimos_estudiantes,
        'periodo_actual': periodo_actual,
    }
    return render(request, 'calificaciones/dashboard.html', context)


# ========== ESTUDIANTES ==========

class ListaEstudiantesView(LoginRequiredMixin, ListView):
    model = Estudiante
    template_name = 'calificaciones/estudiantes/lista.html'
    context_object_name = 'estudiantes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Estudiante.objects.all().order_by('apellido', 'nombre')
        busqueda = self.request.GET.get('q', '')
        if busqueda:
            queryset = queryset.filter(
                Q(codigo__icontains=busqueda) |
                Q(nombre__icontains=busqueda) |
                Q(apellido__icontains=busqueda) |
                Q(cedula__icontains=busqueda) |
                Q(email__icontains=busqueda)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Estudiantes'
        context['busqueda'] = self.request.GET.get('q', '')
        return context


@login_required
def agregar_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estudiante agregado exitosamente.')
            return redirect('calificaciones:lista_estudiantes')
    else:
        form = EstudianteForm()
    
    return render(request, 'calificaciones/estudiantes/agregar.html', {
        'titulo': 'Agregar Estudiante',
        'form': form
    })


@login_required
def editar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id_estudiante=id)
    
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estudiante actualizado exitosamente.')
            return redirect('calificaciones:lista_estudiantes')
    else:
        form = EstudianteForm(instance=estudiante)
    
    return render(request, 'calificaciones/estudiantes/editar.html', {
        'titulo': f'Editar Estudiante: {estudiante.nombre_completo}',
        'form': form,
        'estudiante': estudiante
    })


@login_required
def eliminar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id_estudiante=id)
    
    if request.method == 'POST':
        # Verificar si tiene matrículas
        if Matricula.objects.filter(estudiante=estudiante).exists():
            messages.warning(request, 
                'No se puede eliminar el estudiante porque tiene matrículas asociadas. '
                'Se desactivará en su lugar.'
            )
            estudiante.activo = False
            estudiante.save()
        else:
            estudiante.delete()
            messages.success(request, 'Estudiante eliminado exitosamente.')
        
        return redirect('calificaciones:lista_estudiantes')
    
    return render(request, 'calificaciones/estudiantes/eliminar.html', {
        'titulo': 'Eliminar Estudiante',
        'estudiante': estudiante
    })


# ========== DOCENTES ==========

@login_required
def lista_docentes(request):
    docentes = Docente.objects.all().order_by('apellido', 'nombre')
    
    busqueda = request.GET.get('q', '')
    if busqueda:
        docentes = docentes.filter(
            Q(codigo__icontains=busqueda) |
            Q(nombre__icontains=busqueda) |
            Q(apellido__icontains=busqueda) |
            Q(cedula__icontains=busqueda) |
            Q(email__icontains=busqueda)
        )
    
    context = {
        'docentes': docentes,
        'titulo': 'Lista de Docentes',
        'busqueda': busqueda
    }
    return render(request, 'calificaciones/docentes/lista.html', context)


@login_required
def agregar_docente(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Docente agregado exitosamente.')
            return redirect('calificaciones:lista_docentes')
    else:
        form = DocenteForm()
    
    return render(request, 'calificaciones/docentes/agregar.html', {
        'titulo': 'Agregar Docente',
        'form': form
    })


@login_required
def editar_docente(request, id):
    docente = get_object_or_404(Docente, id_docente=id)
    
    if request.method == 'POST':
        form = DocenteForm(request.POST, instance=docente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Docente actualizado exitosamente.')
            return redirect('calificaciones:lista_docentes')
    else:
        form = DocenteForm(instance=docente)
    
    return render(request, 'calificaciones/docentes/editar.html', {
        'titulo': f'Editar Docente: {docente.nombre_completo}',
        'form': form,
        'docente': docente
    })


# ========== ASIGNATURAS ==========

@login_required
def lista_asignaturas(request):
    asignaturas = Asignatura.objects.all().order_by('codigo')
    
    busqueda = request.GET.get('q', '')
    if busqueda:
        asignaturas = asignaturas.filter(
            Q(codigo__icontains=busqueda) |
            Q(nombre__icontains=busqueda)
        )
    
    context = {
        'asignaturas': asignaturas,
        'titulo': 'Lista de Asignaturas',
        'busqueda': busqueda
    }
    return render(request, 'calificaciones/asignaturas/lista.html', context)


@login_required
def agregar_asignatura(request):
    if request.method == 'POST':
        form = AsignaturaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignatura agregada exitosamente.')
            return redirect('calificaciones:lista_asignaturas')
    else:
        form = AsignaturaForm()
    
    return render(request, 'calificaciones/asignaturas/agregar.html', {
        'titulo': 'Agregar Asignatura',
        'form': form
    })


@login_required
def editar_asignatura(request, id):
    asignatura = get_object_or_404(Asignatura, id_asignatura=id)
    
    if request.method == 'POST':
        form = AsignaturaForm(request.POST, instance=asignatura)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignatura actualizada exitosamente.')
            return redirect('calificaciones:lista_asignaturas')
    else:
        form = AsignaturaForm(instance=asignatura)
    
    return render(request, 'calificaciones/asignaturas/editar.html', {
        'titulo': f'Editar Asignatura: {asignatura.codigo}',
        'form': form,
        'asignatura': asignatura
    })


# ========== PERIODOS ACADÉMICOS ==========

@login_required
def lista_periodos(request):
    periodos = PeriodoAcademico.objects.all().order_by('-fecha_inicio')
    
    context = {
        'periodos': periodos,
        'titulo': 'Períodos Académicos'
    }
    return render(request, 'calificaciones/periodos/lista.html', context)


# ========== CURSOS ==========

@login_required
def lista_cursos(request):
    cursos = Curso.objects.all().select_related('asignatura', 'periodo', 'docente')
    
    periodo_id = request.GET.get('periodo', '')
    asignatura_id = request.GET.get('asignatura', '')
    
    if periodo_id:
        cursos = cursos.filter(periodo_id=periodo_id)
    if asignatura_id:
        cursos = cursos.filter(asignatura_id=asignatura_id)
    
    periodos = PeriodoAcademico.objects.filter(activo=True)
    asignaturas = Asignatura.objects.filter(activo=True)
    
    context = {
        'cursos': cursos,
        'periodos': periodos,
        'asignaturas': asignaturas,
        'titulo': 'Lista de Cursos',
        'periodo_seleccionado': periodo_id,
        'asignatura_seleccionada': asignatura_id
    }
    return render(request, 'calificaciones/cursos/lista.html', context)


@login_required
def agregar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            # Verificar cupo
            if curso.cupo_actual < curso.cupo_maximo:
                form.save()
                messages.success(request, 'Curso creado exitosamente.')
                return redirect('calificaciones:lista_cursos')
            else:
                messages.error(request, 'El cupo máximo ya ha sido alcanzado.')
    else:
        form = CursoForm()
    
    return render(request, 'calificaciones/cursos/agregar.html', {
        'titulo': 'Agregar Curso',
        'form': form
    })


@login_required
def editar_curso(request, id):
    curso = get_object_or_404(Curso, id_curso=id)
    
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso actualizado exitosamente.')
            return redirect('calificaciones:lista_cursos')
    else:
        form = CursoForm(instance=curso)
    
    return render(request, 'calificaciones/cursos/editar.html', {
        'titulo': f'Editar Curso: {curso.asignatura.codigo}-{curso.seccion}',
        'form': form,
        'curso': curso
    })


@login_required
def eliminar_curso(request, id):
    curso = get_object_or_404(Curso, id_curso=id)
    
    if request.method == 'POST':
        # Verificar si tiene matrículas
        if Matricula.objects.filter(curso=curso).exists():
            messages.warning(request, 
                'No se puede eliminar el curso porque tiene matrículas asociadas. '
                'Se desactivará en su lugar.'
            )
            curso.activo = False
            curso.save()
        else:
            curso.delete()
            messages.success(request, 'Curso eliminado exitosamente.')
        
        return redirect('calificaciones:lista_cursos')
    
    return render(request, 'calificaciones/cursos/eliminar.html', {
        'titulo': 'Eliminar Curso',
        'curso': curso
    })


# ========== MATRÍCULAS ==========

@login_required
def lista_matriculas(request):
    matriculas = Matricula.objects.all().select_related(
        'estudiante', 'curso', 'curso__asignatura', 'curso__periodo'
    ).order_by('-fecha_matricula')
    
    # Filtros
    curso_id = request.GET.get('curso', '')
    estado = request.GET.get('estado', '')
    periodo_id = request.GET.get('periodo', '')
    
    if curso_id:
        matriculas = matriculas.filter(curso_id=curso_id)
    if estado:
        matriculas = matriculas.filter(estado=estado)
    if periodo_id:
        matriculas = matriculas.filter(curso__periodo_id=periodo_id)
    
    cursos = Curso.objects.filter(activo=True)
    periodos = PeriodoAcademico.objects.filter(activo=True)
    
    context = {
        'matriculas': matriculas,
        'cursos': cursos,
        'periodos': periodos,
        'titulo': 'Lista de Matrículas',
        'curso_seleccionado': curso_id,
        'estado_seleccionado': estado,
        'periodo_seleccionado': periodo_id
    }
    return render(request, 'calificaciones/matriculas/lista.html', context)


@login_required
def agregar_matricula(request):
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save(commit=False)
            # Verificar cupo del curso
            curso = matricula.curso
            if curso.cupo_actual < curso.cupo_maximo:
                # Verificar si ya está matriculado
                if Matricula.objects.filter(
                    estudiante=matricula.estudiante,
                    curso=matricula.curso
                ).exists():
                    messages.error(request, 'El estudiante ya está matriculado en este curso.')
                else:
                    matricula.save()
                    # Actualizar cupo del curso
                    curso.cupo_actual += 1
                    curso.save()
                    messages.success(request, 'Matrícula realizada exitosamente.')
                    return redirect('calificaciones:lista_matriculas')
            else:
                messages.error(request, 'El curso ha alcanzado su cupo máximo.')
    else:
        form = MatriculaForm()
    
    return render(request, 'calificaciones/matriculas/agregar.html', {
        'titulo': 'Agregar Matrícula',
        'form': form
    })


@login_required
def editar_matricula(request, id):
    matricula = get_object_or_404(Matricula, id_matricula=id)
    
    if request.method == 'POST':
        form = MatriculaForm(request.POST, instance=matricula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matrícula actualizada exitosamente.')
            return redirect('calificaciones:lista_matriculas')
    else:
        form = MatriculaForm(instance=matricula)
    
    return render(request, 'calificaciones/matriculas/editar.html', {
        'titulo': f'Editar Matrícula #{matricula.id_matricula}',
        'form': form,
        'matricula': matricula
    })


@login_required
def eliminar_matricula(request, id):
    matricula = get_object_or_404(Matricula, id_matricula=id)
    
    if request.method == 'POST':
        # Actualizar cupo del curso
        curso = matricula.curso
        if curso.cupo_actual > 0:
            curso.cupo_actual -= 1
            curso.save()
        
        matricula.delete()
        messages.success(request, 'Matrícula eliminada exitosamente.')
        return redirect('calificaciones:lista_matriculas')
    
    return render(request, 'calificaciones/matriculas/eliminar.html', {
        'titulo': 'Eliminar Matrícula',
        'matricula': matricula
    })


# ========== CONFIGURACIÓN DE EVALUACIÓN ==========

@login_required
def configuracion_evaluacion(request, asignatura_id):
    asignatura = get_object_or_404(Asignatura, id_asignatura=asignatura_id)
    configuraciones = ConfiguracionEvaluacion.objects.filter(asignatura=asignatura, activo=True)
    
    # Calcular total de porcentaje
    total_porcentaje = configuraciones.aggregate(Sum('porcentaje'))['porcentaje__sum'] or 0
    
    if request.method == 'POST':
        form = ConfiguracionEvaluacionForm(request.POST)
        if form.is_valid():
            config = form.save(commit=False)
            config.asignatura = asignatura
            
            # Verificar que no exceda el 100%
            nuevo_total = total_porcentaje + config.porcentaje
            if nuevo_total > 100:
                messages.error(request, 
                    f'El porcentaje total no puede exceder 100%. '
                    f'Actual: {total_porcentaje}% + Nuevo: {config.porcentaje}% = {nuevo_total}%'
                )
            else:
                config.save()
                messages.success(request, 'Configuración agregada exitosamente.')
                return redirect('calificaciones:configuracion_evaluacion', asignatura_id=asignatura_id)
    else:
        form = ConfiguracionEvaluacionForm(initial={'asignatura': asignatura})
    
    context = {
        'asignatura': asignatura,
        'configuraciones': configuraciones,
        'form': form,
        'total_porcentaje': total_porcentaje,
        'titulo': f'Configuración de Evaluación - {asignatura.nombre}'
    }
    return render(request, 'calificaciones/configuracion/lista.html', context)


@login_required
def eliminar_configuracion(request, config_id):
    configuracion = get_object_or_404(ConfiguracionEvaluacion, id_config=config_id)
    asignatura_id = configuracion.asignatura.id_asignatura
    
    if request.method == 'POST':
        configuracion.delete()
        messages.success(request, 'Configuración eliminada exitosamente.')
        return redirect('calificaciones:configuracion_evaluacion', asignatura_id=asignatura_id)
    
    return render(request, 'calificaciones/configuracion/eliminar.html', {
        'titulo': 'Eliminar Configuración',
        'configuracion': configuracion
    })


# ========== CALIFICACIONES ==========

@login_required
def lista_calificaciones(request):
    calificaciones = Calificacion.objects.all().select_related(
        'matricula__estudiante',
        'matricula__curso__asignatura',
        'configuracion'
    ).order_by('-fecha_registro')
    
    # Filtros
    curso_id = request.GET.get('curso', '')
    estudiante_id = request.GET.get('estudiante', '')
    
    if curso_id:
        calificaciones = calificaciones.filter(matricula__curso_id=curso_id)
    if estudiante_id:
        calificaciones = calificaciones.filter(matricula__estudiante_id=estudiante_id)
    
    cursos = Curso.objects.filter(activo=True)
    estudiantes = Estudiante.objects.filter(activo=True)
    
    context = {
        'calificaciones': calificaciones,
        'cursos': cursos,
        'estudiantes': estudiantes,
        'titulo': 'Lista de Calificaciones',
        'curso_seleccionado': curso_id,
        'estudiante_seleccionado': estudiante_id
    }
    return render(request, 'calificaciones/calificaciones/lista.html', context)


@login_required
def agregar_calificacion(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.registrado_por = request.user
            calificacion.save()
            
            # Actualizar nota final del estudiante en esa matrícula
            actualizar_nota_final(calificacion.matricula)
            
            messages.success(request, 'Calificación registrada exitosamente.')
            return redirect('calificaciones:lista_calificaciones')
    else:
        form = CalificacionForm()
    
    return render(request, 'calificaciones/calificaciones/agregar.html', {
        'titulo': 'Agregar Calificación',
        'form': form
    })


@login_required
def editar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id_calificacion=id)
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            
            # Actualizar nota final
            actualizar_nota_final(calificacion.matricula)
            
            messages.success(request, 'Calificación actualizada exitosamente.')
            return redirect('calificaciones:lista_calificaciones')
    else:
        form = CalificacionForm(instance=calificacion)
    
    return render(request, 'calificaciones/calificaciones/editar.html', {
        'titulo': f'Editar Calificación #{calificacion.id_calificacion}',
        'form': form,
        'calificacion': calificacion
    })


@login_required
def gestionar_calificaciones(request):
    """Vista para gestionar calificaciones masivas"""
    if request.method == 'GET':
        curso_id = request.GET.get('curso', '')
        configuracion_id = request.GET.get('configuracion', '')
        
        if curso_id and configuracion_id:
            curso = get_object_or_404(Curso, id_curso=curso_id)
            configuracion = get_object_or_404(ConfiguracionEvaluacion, id_config=configuracion_id)
            
            # Obtener estudiantes matriculados
            matriculas = Matricula.objects.filter(
                curso=curso,
                estado='matriculado'
            ).select_related('estudiante')
            
            # Obtener calificaciones existentes
            calificaciones_existentes = Calificacion.objects.filter(
                configuracion=configuracion,
                matricula__in=matriculas
            )
            
            context = {
                'curso': curso,
                'configuracion': configuracion,
                'matriculas': matriculas,
                'calificaciones_existentes': calificaciones_existentes,
                'titulo': f'Gestionar Calificaciones - {configuracion.nombre_evaluacion}'
            }
            return render(request, 'calificaciones/calificaciones/gestionar.html', context)
    
    # Si no hay filtros, mostrar formulario de selección
    cursos = Curso.objects.filter(activo=True)
    configuraciones = ConfiguracionEvaluacion.objects.filter(activo=True)
    
    context = {
        'cursos': cursos,
        'configuraciones': configuraciones,
        'titulo': 'Gestionar Calificaciones'
    }
    return render(request, 'calificaciones/calificaciones/gestionar_form.html', context)


@login_required
def get_calificacion_estudiante(request):
    """API para obtener calificación de un estudiante"""
    if request.method == 'GET':
        matricula_id = request.GET.get('matricula_id')
        configuracion_id = request.GET.get('configuracion_id')
        
        try:
            calificacion = Calificacion.objects.get(
                matricula_id=matricula_id,
                configuracion_id=configuracion_id
            )
            return JsonResponse({
                'existe': True,
                'nota': float(calificacion.nota),
                'observaciones': calificacion.observaciones
            })
        except Calificacion.DoesNotExist:
            return JsonResponse({'existe': False})
    
    return JsonResponse({'error': 'Método no permitido'}, status=400)


# ========== REPORTES ==========

@login_required
def reportes(request):
    """Página principal de reportes"""
    periodos = PeriodoAcademico.objects.filter(activo=True)
    cursos = Curso.objects.filter(activo=True)
    estudiantes = Estudiante.objects.filter(activo=True)
    
    context = {
        'periodos': periodos,
        'cursos': cursos,
        'estudiantes': estudiantes,
        'titulo': 'Reportes'
    }
    return render(request, 'calificaciones/reportes/index.html', context)


@login_required
def boleta_calificaciones(request):
    """Boleta de calificaciones para un estudiante"""
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante')
        periodo_id = request.POST.get('periodo')
        
        if estudiante_id and periodo_id:
            estudiante = get_object_or_404(Estudiante, id_estudiante=estudiante_id)
            periodo = get_object_or_404(PeriodoAcademico, id_periodo=periodo_id)
            
            # Obtener matrículas del estudiante en el período
            matriculas = Matricula.objects.filter(
                estudiante=estudiante,
                curso__periodo=periodo,
                estado='matriculado'
            ).select_related('curso', 'curso__asignatura')
            
            # Obtener calificaciones para cada matrícula
            datos_cursos = []
            for matricula in matriculas:
                calificaciones = Calificacion.objects.filter(
                    matricula=matricula
                ).select_related('configuracion')
                
                # Calcular nota final ponderada
                nota_final = 0
                for cal in calificaciones:
                    nota_final += cal.nota_ponderada
                
                datos_cursos.append({
                    'matricula': matricula,
                    'calificaciones': calificaciones,
                    'nota_final': round(nota_final, 2)
                })
            
            context = {
                'estudiante': estudiante,
                'periodo': periodo,
                'datos_cursos': datos_cursos,
                'fecha_actual': datetime.now(),
                'titulo': f'Boleta de Calificaciones - {estudiante.nombre_completo}'
            }
            return render(request, 'calificaciones/reportes/boleta.html', context)
    
    # Si no es POST, redirigir al formulario
    return redirect('calificaciones:reportes')


@login_required
def generar_reporte_individual_pdf(request, estudiante_id):
    """Genera PDF de reporte individual"""
    # Aquí iría la lógica para generar PDF
    # Puedes usar reportlab, weasyprint, o xhtml2pdf
    estudiante = get_object_or_404(Estudiante, id_estudiante=estudiante_id)
    
    # Por ahora solo redirigimos a la vista HTML
    messages.info(request, 'Generación de PDF en desarrollo')
    return redirect('calificaciones:reportes')


@login_required
def generar_reporte_grupo_pdf(request):
    """Genera PDF de reporte grupal"""
    if request.method == 'POST':
        curso_id = request.POST.get('curso')
        # Lógica para generar PDF grupal
        messages.info(request, 'Generación de PDF grupal en desarrollo')
    
    return redirect('calificaciones:reportes')


# ========== AUTENTICACIÓN ==========

def registro_docente(request):
    """Registro de nuevos docentes"""
    if request.method == 'POST':
        form = RegistroDocenteForm(request.POST)
        if form.is_valid():
            # Crear usuario
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['nombre'],
                last_name=form.cleaned_data['apellido']
            )
            
            # Crear perfil de docente
            Docente.objects.create(
                usuario=user,
                codigo=form.cleaned_data['codigo'],
                cedula=form.cleaned_data['cedula'],
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                email=form.cleaned_data['email'],
                especialidad=form.cleaned_data.get('especialidad', '')
            )
            
            messages.success(request, 'Docente registrado exitosamente. Ahora puede iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroDocenteForm()
    
    return render(request, 'calificaciones/auth/registro.html', {
        'titulo': 'Registro de Docente',
        'form': form
    })


# ========== FUNCIONES AUXILIARES ==========

def actualizar_nota_final(matricula):
    """Calcula y actualiza la nota final de una matrícula"""
    calificaciones = Calificacion.objects.filter(matricula=matricula)
    
    if calificaciones.exists():
        # Calcular nota final ponderada
        nota_final = 0
        for cal in calificaciones:
            nota_final += cal.nota_ponderada
        
        matricula.nota_final = round(nota_final, 2)
        
        # Determinar estado basado en nota final
        if nota_final >= 60:
            matricula.estado = 'aprobado'
        elif nota_final >= 40:
            matricula.estado = 'reprobado'
        else:
            matricula.estado = 'incompleto'
        
        matricula.save()
def login_view(request):
    """Vista personalizada para login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('calificaciones:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'registration/login.html')

def logout_view(request):
    """Vista personalizada para logout"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('calificaciones:login')

        