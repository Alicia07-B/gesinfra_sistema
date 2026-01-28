# calificaciones/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        }

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'
 
class AsignaturaForm(forms.ModelForm):
    # Campo de horas_semana definido EXPLÍCITAMENTE
    horas_semana = forms.ChoiceField(
        choices=[
            ('', 'Seleccione horas semanales'),
            ('2', '2 horas'),
            ('3', '3 horas'),
            ('4', '4 horas'),
            ('5', '5 horas'),
            ('6', '6 horas'),
            ('7', '7 horas'),
            ('8', '8 horas'),
            ('9', '9 horas'),
            ('10', '10 horas'),
        ],
        label="Horas semanales",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    class Meta:
        model = Asignatura
        # Especifica TODOS los campos que existen en tu modelo
        fields = ['codigo', 'nombre', 'horas_semana', 'descripcion', 'activo']
        # Si tienes curso y configuracionevaluacion, inclúyelos:
        # fields = ['codigo', 'nombre', 'horas_semana', 'descripcion', 'activo', 'curso', 'configuracionevaluacion']
        
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: MAT-101'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Matemáticas Básicas'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción de la asignatura...'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch'
            }),
        }
        labels = {
            'codigo': 'Código',
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'activo': 'Activa',
        }


class CursoForm(forms.ModelForm):
    # Si el campo periodo ahora es una ForeignKey a PeriodoAcademico
    periodo_academico = forms.ModelChoiceField(
        queryset=PeriodoAcademico.objects.filter(activo=True),
        label="Período Académico",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Campo para sección como desplegable
    SECCIONES_CHOICES = [
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    
    seccion = forms.ChoiceField(
        choices=SECCIONES_CHOICES,
        label="Sección",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Curso
        fields = ['asignatura', 'periodo_academico', 'docente', 'seccion', 
                  'cupo_maximo', 'cupo_actual', 'aula', 'horario', 
                  'dias_clase', 'activo']
        widgets = {
            'asignatura': forms.Select(attrs={'class': 'form-select'}),
            'docente': forms.Select(attrs={'class': 'form-select'}),
            'cupo_maximo': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'cupo_actual': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'aula': forms.TextInput(attrs={'class': 'form-control'}),
            'horario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08:00-10:00'}),
            'dias_clase': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estás editando un curso existente, mostrar el período actual
        if self.instance and self.instance.pk:
            if hasattr(self.instance, 'periodo_academico'):
                self.fields['periodo_academico'].initial = self.instance.periodo_academico
        
        # Ordenar asignaturas alfabéticamente
        self.fields['asignatura'].queryset = self.fields['asignatura'].queryset.order_by('nombre')
        
        # Filtrar docentes activos
        self.fields['docente'].queryset = self.fields['docente'].queryset.filter(activo=True).order_by('apellido')


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
    

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = '__all__'
        widgets = {
            'fecha_matricula': forms.DateInput(attrs={'type': 'date'}),
        }

class ConfiguracionEvaluacionForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionEvaluacion
        fields = '__all__'

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = '__all__'
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        }

class RegistroDocenteForm(UserCreationForm):
    email = forms.EmailField(required=True)
    codigo = forms.CharField(max_length=20, required=True)
    cedula = forms.CharField(max_length=20, required=True)
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    especialidad = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        
        if commit:
            user.save()
        return user
