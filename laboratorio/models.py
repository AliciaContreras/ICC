from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# --- Entidad Independiente ---
class MaterialSospechoso(models.Model):
    PELIGROSIDAD = [
        ('BAJO', 'Bajo - Causa picazón'),
        ('MEDIO', 'Medio - Inflamable'),
        ('ALTO', 'Alto - Radioactivo'),
        ('EXTREMO', 'Extremo - Fin del mundo'),
    ]

    nombre = models.CharField(max_length=100)
    # Agrega choices=PELIGROSIDAD:
    nivel_peligro = models.CharField(max_length=20, choices=PELIGROSIDAD, default='BAJO')
    es_ilegal = models.BooleanField(default=True)
    stock_gramos = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

# --- Relación 1 a Muchos (1:N) ---
class Cientifico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)
    foto = models.ImageField(upload_to='cientificos/', blank=True, null=True)


    def __str__(self):
        return self.nombre

class Esbirro(models.Model):
    cientifico = models.ForeignKey(Cientifico, on_delete=models.CASCADE, related_name='esbirros')
    nombre = models.CharField(max_length=100)
    tiene_joroba = models.BooleanField(default=True) 
    nivel_lealtad = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)] # Validador extra de seguridad
    )

    def __str__(self):
        return f"{self.nombre} (Jefe: {self.cientifico.nombre})"

# --- Relación Muchos a Muchos (N:N) ---
class Componente(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Invento(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    probabilidad_exito = models.IntegerField(
        help_text="Porcentaje de 0 a 100",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    foto = models.ImageField(upload_to='inventos/', blank=True, null=True)
    # Campo para demostrar migraciones 
    fecha_fabricacion = models.DateField(default=timezone.now) 
    
    componentes = models.ManyToManyField(Componente, through='Receta')

    def __str__(self):
        return self.nombre

class Receta(models.Model):
    invento = models.ForeignKey(Invento, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

# --- Relación 1 a 1 (1:1) ---
class ProtocoloAutodestruccion(models.Model):
    invento = models.OneToOneField(Invento, on_delete=models.CASCADE, primary_key=True)
    codigo_activacion = models.CharField(max_length=20)
    mensaje_despedida = models.CharField(max_length=100)