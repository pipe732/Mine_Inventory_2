from django.db import models
class CategoriaHerramienta(models.Model):
    nombre = models.CharField(max_length=100)  

    ESTADO_CHOICES = [
        ('Herramienta', 'Herramienta'),
        ('Maquinaria', 'Maquinaria'),
        ('Equipo de Protección Personal', 'Equipo de Protección Personal'),
        ('Consumible', 'Consumible'),
        ('Otro', 'Otro'),
    ]

    def __str__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Stock(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('prestado',   'Prestado'),
        ('dañado',     'Dañado'),
        ('baja',       'De baja'),
    ]

    codigo        = models.CharField(max_length=50, unique=True, verbose_name="Código único")
    herramienta   = models.CharField(max_length=150, verbose_name="Nombre de herramienta")
    categoria     = models.ForeignKey(
                        CategoriaHerramienta,
                        on_delete=models.SET_NULL,
                        null=True, blank=True,
                        verbose_name="Categoría"
                    )
    ubicacion     = models.CharField(max_length=150, verbose_name="Ubicación en la mina")
    estado        = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    proveedor  = models.CharField(max_length=150, verbose_name="Proveedor", blank=True, null=True)  # ← NUEVO
    fecha_ingreso = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} – {self.herramienta}"

    class Meta:
        verbose_name = "Herramienta"
        verbose_name_plural = "Herramientas"
        ordering = ['codigo']
        
class Proveedor(models.Model):
    nit = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    numero = models.CharField(max_length=20)
    correo = models.EmailField()
    que_provee = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre