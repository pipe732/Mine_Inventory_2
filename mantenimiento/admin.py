from django.contrib import admin
from .models import BitacoraEstado, BitacoraMantenimiento, DetalleMantenimiento

# Esto permite agregar detalles directamente dentro de la bitácora de mantenimiento
class DetalleInline(admin.TabularInline):
    model = DetalleMantenimiento
    extra = 1

@admin.register(BitacoraMantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('id_mantenimiento', 'tipo_mantenimiento', 'id_bitacora_estado')
    inlines = [DetalleInline]

admin.site.register(BitacoraEstado)
