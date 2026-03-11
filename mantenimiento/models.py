# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
'''
creamos las tablas del modulo con sus respectivos atributos 
creamos la tabla bitacora de estado
modulos de Albert bitacora estado, Bitacora de mantenimiento, Detalle mantenimiento
'''
class BitacoraEstado(models.Model):
    #clasificamos el estado de las herramientas con tres opciones a elegirt
    OPCIONES_ESTADO = [
        ('operativo', 'Operativo (Funcional)'),
        ('mantenimiento', 'En Mantenimiento'),
        ('limitado', 'Uso Limitado (Desgaste Medio)'),
        ('critico', 'Estado Crítico (Falla Inminente)'),
        ('fuera_servicio', 'Fuera de Servicio (Dañado)'),
        ('baja', 'Baja Definitiva (No Reparable)'),
    ]
    id_bitacora_estado = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    estado = models.CharField(
        max_length=50,
        choices=OPCIONES_ESTADO,
        default='operativo'
    )
    nivel_estado = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Escala del 1 (Pésimo) al 10 (Nuevo)"
    )
    class Meta:
        verbose_name = "Bitácora de Estado"
        verbose_name_plural = "Bitácoras de Estado"
    def __str__(self):
        return f"{self.get_estado_display()} - Nivel {self.nivel_estado}"
class BitacoraMantenimiento(models.Model):
    #agregamos menu desplegable con tres opciones

    OPCIONES_TIPO = [
        ('correctivo', 'Correctivo'),
        ('preventivo', 'Preventivo'),
        ('reparable', 'Reparable'),
    ]
    id_mantenimiento = models.AutoField(primary_key=True)
    id_bitacora_estado = models.ForeignKey(
        BitacoraEstado, 
        on_delete=models.PROTECT, 
        related_name='mantenimientos'
    )
    tipo_mantenimiento = models.CharField(
        max_length=100, 
        choices=OPCIONES_TIPO, 
        default='preventivo'
    )
    class Meta:
        verbose_name = "Bitácora de Mantenimiento"
    def __str__(self):
        return f"Mantenimiento {self.id_mantenimiento} ({self.get_tipo_mantenimiento_display()})"  
class DetalleMantenimiento(models.Model):
    id_detalle_mantenimiento = models.AutoField(primary_key=True)
    id_mantenimiento = models.ForeignKey(
        BitacoraMantenimiento, 
        on_delete=models.CASCADE, 
        related_name='detalles'
    )  
    #campo para descripcion del mantenimiento
    motivo_mantenimiento = models.CharField(
        max_length=255, 
        help_text="Escriba brevemente el motivo de este detalle (ej: Desgaste de pieza)"
    ) 
    descripcion = models.TextField(help_text="Descripción detallada del trabajo realizado")
    tipo = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Detalle de Mantenimiento"
        verbose_name_plural = "Detalles de Mantenimientos"
    
