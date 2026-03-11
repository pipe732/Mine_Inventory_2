from django.contrib import admin
from .models import CategoriaHerramienta, Stock


@admin.register(CategoriaHerramienta)
class CategoriaHerramientaAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('nombre',)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display  = ('codigo', 'herramienta', 'categoria', 'ubicacion', 'estado', 'fecha_ingreso')
    list_filter   = ('estado', 'categoria')
    search_fields = ('codigo', 'herramienta', 'observaciones')
    readonly_fields = ('fecha_ingreso',)
    ordering      = ('codigo',)
    fieldsets = (
        ('Identificación', {
            'fields': ('codigo', 'herramienta', 'categoria')
        }),
        ('Detalles', {
            'fields': ('ubicacion', 'estado', 'fecha_ingreso', 'observaciones')
        }),
    )
# Register your models here.
