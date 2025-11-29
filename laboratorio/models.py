import os
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# --- UTILIDAD: Renombrado de imágenes ---
def generar_nombre_unico(instance, filename):
    """
    Genera un nombre aleatorio (UUID) para evitar colisiones de archivos,
    manteniendo la extensión original (.jpg, .png).
    Guarda en carpetas según el modelo: 'fotos_cientificos/' o 'fotos_inventos/'
    """
    extension = filename.split('.')[-1]
    nombre_nuevo = f"{uuid.uuid4()}.{extension}"
    # instance.__class__.__name__  da "Cientifico" o "Invento"
    carpeta = f"fotos_{instance.__class__.__name__.lower()}s"
    return os.path.join(carpeta, nombre_nuevo)


# --- Entidad Independiente ---
class MaterialSospechoso(models.Model):
    PELIGROSIDAD = [
        ('BAJO', 'Bajo - Causa picazón'),
        ('MEDIO', 'Medio - Inflamable'),
        ('ALTO', 'Alto - Radioactivo'),
        ('EXTREMO', 'Extremo - Fin del mundo'),
    ]

    nombre = models.CharField(max_length=100)
    nivel_peligro = models.CharField(max_length=20, choices=PELIGROSIDAD, default='BAJO')
    es_ilegal = models.BooleanField(default=True)
    stock_gramos = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        legalidad = "Ilegal" if self.es_ilegal else "Legal"
        return f"{self.nombre} ({self.get_nivel_peligro_display()} - {legalidad})"


# --- Relación 1 a Muchos (1:N) ---
class Cientifico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)
    # MEJORA: Se usa la función para renombrar archivos
    foto = models.ImageField(upload_to=generar_nombre_unico, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Esbirro(models.Model):
    cientifico = models.ForeignKey(Cientifico, on_delete=models.CASCADE, related_name='esbirros')
    nombre = models.CharField(max_length=100)
    tiene_joroba = models.BooleanField(default=True) 
    nivel_lealtad = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def clean(self):
        # Lógica de negocio extra (Cláusula de guarda en validación)
        if self.nivel_lealtad < 1:
            raise ValidationError("Un esbirro no puede tener lealtad menor a 1 (se iría con el enemigo).")
        
        if self.nivel_lealtad > 10:
            raise ValidationError("La lealtad no puede superar 10 (nadie es tan fiel).")

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
    # MEJORA: Se usa la función para renombrar archivos
    foto = models.ImageField(upload_to=generar_nombre_unico, blank=True, null=True)
    fecha_fabricacion = models.DateField(default=timezone.now) 
    
    componentes = models.ManyToManyField(Componente, through='Receta')

    def clean(self):
        # Validación cruzada
        if self.probabilidad_exito > 100:
             raise ValidationError({'probabilidad_exito': "No puedes tener más de 100% de éxito, esto es ciencia, no magia."})

    def __str__(self):
        return f"{self.nombre} ({self.probabilidad_exito}% éxito)"


class Receta(models.Model):
    invento = models.ForeignKey(Invento, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    
    class Meta:
        # MEJORA: Evitar duplicados (no se puede tener 2 veces el mismo ingrediente en el mismo invento, solo aumentar la cantidad)
        unique_together = ('invento', 'componente')

    def __str__(self):
        return f"{self.cantidad}x {self.componente.nombre} para {self.invento.nombre}"


# --- Relación 1 a 1 (1:1) ---
class ProtocoloAutodestruccion(models.Model):
    invento = models.OneToOneField(Invento, on_delete=models.CASCADE, primary_key=True)
    codigo_activacion = models.CharField(max_length=20)
    mensaje_despedida = models.CharField(max_length=100)

    def __str__(self):
        return f"Protocolo para {self.invento.nombre}"