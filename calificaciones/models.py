# calificaciones/models.py - TODOS LOS MODELOS AQUÍ
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# ========== ESTUDIANTE ==========
class Estudiante(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=1, choices=[
        ('M', 'Masculino'), 
        ('F', 'Femenino'), 
        ('O', 'Otro')
    ], blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre_completo()}"
    
    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

# ========== DOCENTE ==========
class Docente(models.Model):
    id_docente = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    codigo = models.CharField(max_length=20, unique=True)
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre_completo()}"
    
    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'

# ========== ASIGNATURA ==========
class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    horas_semana = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'

# ========== PERIODO ACADÉMICO ==========
class PeriodoAcademico(models.Model):
    id_periodo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Período Académico'
        verbose_name_plural = 'Períodos Académicos'

# ========== CURSO ==========
class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, blank=True, null=True)
    seccion = models.CharField(max_length=10)
    cupo_maximo = models.IntegerField(default=30)
    cupo_actual = models.IntegerField(default=0)
    horario = models.CharField(max_length=100, blank=True, null=True)
    aula = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.codigo} - Sección {self.seccion}"
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        unique_together = ['asignatura', 'periodo', 'seccion']

# ========== MATRÍCULA ==========
class Matricula(models.Model):
    id_matricula = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_matricula = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('matriculado', 'Matriculado'),
        ('aprobado', 'Aprobado'),
        ('reprobado', 'Reprobado'),
        ('incompleto', 'Incompleto'),
    ], default='matriculado')
    nota_final = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"Matrícula {self.id_matricula} - {self.estudiante.nombre_completo()}"
    
    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        unique_together = ['estudiante', 'curso']

# ========== CONFIGURACIÓN EVALUACIÓN ==========
class ConfiguracionEvaluacion(models.Model):
    id_config = models.AutoField(primary_key=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    nombre_evaluacion = models.CharField(max_length=100)
    porcentaje = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre_evaluacion} ({self.porcentaje}%)"
    
    class Meta:
        verbose_name = 'Configuración de Evaluación'
        verbose_name_plural = 'Configuraciones de Evaluación'

# ========== CALIFICACIÓN ==========
class Calificacion(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    configuracion = models.ForeignKey(ConfiguracionEvaluacion, on_delete=models.CASCADE)
    nota = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    @property
    def nota_ponderada(self):
        return (self.nota * self.configuracion.porcentaje) / 100
    
    def __str__(self):
        return f"Calificación {self.id_calificacion} - Nota: {self.nota}"
    
    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        unique_together = ['matricula', 'configuracion']

        