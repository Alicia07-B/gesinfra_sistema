# calificaciones/context_processors.py
from .models import PeriodoAcademico

def periodo_actual(request):
    return {
        'periodo_actual': PeriodoAcademico.objects.filter(activo=True).first()
    }
