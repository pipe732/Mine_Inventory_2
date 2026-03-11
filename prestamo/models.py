from django.db import models
from inventario.models import Stock  # Importante para conectar las apps

class Prestamo(models.Model):
    id_prestamo = models.AutoField(primary_key=True)
    # Conectamos con Stock de la app inventario
    herramienta = models.ForeignKey(Stock, on_delete=models.PROTECT, db_column='id_codigo')
    numero_documento = models.ForeignKey(
        'Usuario',
        to_field='numero_documento',
        on_delete=models.PROTECT,
        db_column='numero_documento'
    )
    id_estado = models.ForeignKey(
        'Estado',
        on_delete=models.PROTECT,
        db_column='id_estado'
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'prestamo'
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'

    def __str__(self):
        return f'Préstamo #{self.id_prestamo}'

class DetallePrestamo(models.Model):
    id_detalle_prestamo = models.AutoField(primary_key=True)
    id_prestamo = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE,
        db_column='id_prestamo',
        related_name='detalles'
    )
    herramienta = models.ForeignKey(Stock, on_delete=models.PROTECT, db_column='id_codigo')
    cantidad = models.PositiveIntegerField()

    class Meta:
        db_table = 'detalle_prestamo'
        verbose_name = 'Detalle de Préstamo'
        verbose_name_plural = 'Detalles de Préstamo'

    def __str__(self):
        return f'Detalle #{self.id_detalle_prestamo} - Préstamo #{self.id_prestamo_id}'

# CAMBIADO: De Devolucioncodigo a DevolucionHerramienta para que coincida con admin.py
class DevolucionHerramienta(models.Model):
    id_devolucion_codigo = models.AutoField(primary_key=True)
    id_detalle_prestamo = models.ForeignKey(
        DetallePrestamo,
        on_delete=models.PROTECT,
        db_column='id_detalle_prestamo',
        related_name='devoluciones'
    )
    herramienta = models.ForeignKey(Stock, on_delete=models.PROTECT, db_column='id_codigo')
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'devolucion_codigo'
        verbose_name = 'Devolución de Herramienta'
        verbose_name_plural = 'Devoluciones de Herramientas'

    def __str__(self):
        return f'Devolución #{self.id_devolucion_codigo}'

# Modelos de referencia
class Usuario(models.Model):
    numero_documento = models.CharField(max_length=20, primary_key=True)
    id_rol = models.ForeignKey('Rol', on_delete=models.PROTECT, db_column='id_rol')
    nombre_completo = models.CharField(max_length=150)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    tipo_documento = models.CharField(max_length=50)

    class Meta:
        db_table = 'usuario'
    def __str__(self):
        return self.nombre_completo

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    class Meta:
        db_table = 'rol'
    def __str__(self):
        return self.nombre

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    class Meta:
        db_table = 'estado'
    def __str__(self):
        return self.nombre