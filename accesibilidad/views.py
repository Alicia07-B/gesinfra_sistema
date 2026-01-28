from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import InstitucionEducativa, EncuestaBarreras
from .forms import InstitucionForm, EncuestaBarrerasForm

# ===== DASHBOARD =====
def dashboard(request):
    instituciones = InstitucionEducativa.objects.all().order_by('-fecha_registro')[:5]
    encuestas = EncuestaBarreras.objects.all().order_by('-fecha_registro')[:5]
    
    context = {
        'instituciones': instituciones,
        'encuestas': encuestas,
        'total_instituciones': InstitucionEducativa.objects.count(),
        'total_encuestas': EncuestaBarreras.objects.count(),
    }
    return render(request, 'accesibilidad/dashboard.html', context)

# ===== INSTITUCIONES =====
def nueva_institucion(request):
    if request.method == 'POST':
        form = InstitucionForm(request.POST)
        if form.is_valid():
            try:
                institucion = form.save()
                messages.success(request, f'¡Institución "{institucion.nombre_institucion}" registrada exitosamente!')
                return redirect('lista_instituciones')
            except IntegrityError:
                messages.error(request, 'Ya existe una institución con ese código AMIE')
            except Exception as e:
                messages.error(request, f'Error al guardar: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = InstitucionForm()
    
    return render(request, 'accesibilidad/instituciones/nueva.html', {'form': form})

def lista_instituciones(request):
    try:
        # Obtener todas las instituciones ordenadas por nombre
        instituciones = InstitucionEducativa.objects.all().order_by('nombre_institucion')
        
        context = {
            'instituciones': instituciones,
            'titulo': 'Instituciones Educativas'
        }
        
        return render(request, 'accesibilidad/instituciones/lista.html', context)
        
    except Exception as e:
        # Si hay error, mostrar mensaje y redirigir
        messages.error(request, f'Error al cargar las instituciones: {str(e)}')
        return redirect('dashboard_accesibilidad')

def detalle_institucion(request, institucion_id):
    institucion = get_object_or_404(InstitucionEducativa, id=institucion_id)
    encuestas = EncuestaBarreras.objects.filter(institucion=institucion)
    
    context = {
        'institucion': institucion,
        'encuestas': encuestas,
    }
    return render(request, 'accesibilidad/instituciones/detalle.html', context)

# ===== ENCUESTAS =====
def seleccionar_institucion(request):
    instituciones = InstitucionEducativa.objects.all().order_by('nombre_institucion')
    
    if request.method == 'POST':
        institucion_id = request.POST.get('institucion_id')
        if institucion_id:
            # Guardar en sesión para el siguiente paso
            request.session['institucion_id'] = institucion_id
            return redirect('crear_encuesta')
    
    context = {
        'instituciones': instituciones,
        'titulo': 'Seleccionar Institución para Encuesta'
    }
    return render(request, 'accesibilidad/encuestas/seleccionar_institucion.html', context)

def crear_encuesta(request):
    # Verificar si hay institución seleccionada
    institucion_id = request.session.get('institucion_id')
    if not institucion_id:
        messages.warning(request, 'Por favor seleccione una institución primero')
        return redirect('seleccionar_institucion')
    
    institucion = get_object_or_404(InstitucionEducativa, id=institucion_id)
    
    if request.method == 'POST':
        form = EncuestaBarrerasForm(request.POST)
        if form.is_valid():
            try:
                # Crear la encuesta manualmente con los datos del formulario
                encuesta = EncuestaBarreras.objects.create(
                    institucion=institucion,
                    fecha_encuesta=form.cleaned_data['fecha_encuesta'],
                    encuestador=form.cleaned_data['encuestador'] or None,
                    cargo_encuestador=form.cleaned_data['cargo_encuestador'] or None,
                    p1_accesos=form.cleaned_data['p1_accesos'],
                    p2_pasillos=form.cleaned_data['p2_pasillos'],
                    p3_rampas=form.cleaned_data['p3_rampas'],
                    p4_banos=form.cleaned_data['p4_banos'],
                    p5_puertas=form.cleaned_data['p5_puertas'],
                    p6_senialetica=form.cleaned_data['p6_senialetica'],
                    p7_iluminacion=form.cleaned_data['p7_iluminacion'],
                    p8_equipos=form.cleaned_data['p8_equipos'],
                    p9_internet=form.cleaned_data['p9_internet'],
                    p10_software=form.cleaned_data['p10_software'],
                    p11_plataformas=form.cleaned_data['p11_plataformas'],
                    p12_capacitacion=form.cleaned_data['p12_capacitacion'],
                    p13_soporte=form.cleaned_data['p13_soporte'],
                    p14_recursos=form.cleaned_data['p14_recursos'],
                    observaciones=form.cleaned_data['observaciones'] or None,
                    recomendaciones=form.cleaned_data['recomendaciones'] or None,
                )
                
                # Limpiar sesión
                if 'institucion_id' in request.session:
                    del request.session['institucion_id']
                
                messages.success(request, f'¡Encuesta para {institucion.nombre_institucion} creada exitosamente!')
                return redirect('lista_encuestas')
                
            except Exception as e:
                messages.error(request, f'Error al guardar la encuesta: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = EncuestaBarrerasForm()
    
    context = {
        'institucion': institucion,
        'form': form,
    }
    
    return render(request, 'accesibilidad/encuestas/crear.html', context)
def lista_encuestas(request):
    encuestas = EncuestaBarreras.objects.all().order_by('-fecha_encuesta')
    return render(request, 'accesibilidad/encuestas/lista.html', {'encuestas': encuestas})

def detalle_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(EncuestaBarreras, id=encuesta_id)
    
    # Organizar preguntas para mostrar
    preguntas_fisicas = [
        {'numero': 1, 'texto': 'Los accesos principales al edificio (puertas, rampas) son fáciles de usar...', 'respuesta': encuesta.p1_accesos},
        {'numero': 2, 'texto': 'Los pasillos, aulas y espacios comunes están libres de obstáculos...', 'respuesta': encuesta.p2_pasillos},
        {'numero': 3, 'texto': 'Existen y están disponibles rampas o elevadores...', 'respuesta': encuesta.p3_rampas},
        {'numero': 4, 'texto': 'Los baños son accesibles, cuentan con señales claras...', 'respuesta': encuesta.p4_banos},
        {'numero': 5, 'texto': 'Las aulas tienen una iluminación y ventilación adecuadas...', 'respuesta': encuesta.p5_puertas},
        {'numero': 6, 'texto': 'La señalización (letreros, pictogramas) en el edificio...', 'respuesta': encuesta.p6_senialetica},
        {'numero': 7, 'texto': 'El mobiliario (sillas, mesas) es ajustable...', 'respuesta': encuesta.p7_iluminacion},
    ]
    
    preguntas_tecnologicas = [
        {'numero': 8, 'texto': 'La institución cuenta con equipos tecnológicos...', 'respuesta': encuesta.p8_equipos},
        {'numero': 9, 'texto': 'La conexión a internet es estable, rápida...', 'respuesta': encuesta.p9_internet},
        {'numero': 10, 'texto': 'Las plataformas y software educativos utilizados...', 'respuesta': encuesta.p10_software},
        {'numero': 11, 'texto': 'Los docentes y personal administrativo reciben...', 'respuesta': encuesta.p11_plataformas},
        {'numero': 12, 'texto': 'Los estudiantes con necesidades específicas...', 'respuesta': encuesta.p12_capacitacion},
        {'numero': 13, 'texto': 'Existe soporte técnico adecuado...', 'respuesta': encuesta.p13_soporte},
        {'numero': 14, 'texto': 'Los recursos digitales educativos...', 'respuesta': encuesta.p14_recursos},
    ]
    
    context = {
        'encuesta': encuesta,
        'preguntas_fisicas': preguntas_fisicas,
        'preguntas_tecnologicas': preguntas_tecnologicas,
    }
    
    return render(request, 'accesibilidad/encuestas/detalle.html', context)