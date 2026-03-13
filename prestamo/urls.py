# prestamo/urls.py
from django.urls import path
from .views import (
    prestamo_list_view, # CAMBIADO para coincidir con el nuevo nombre
    prestamo_create, 
    prestamo_edit, 
    prestamo_delete, 
    devolucion_create
)

urlpatterns = [
    # El nombre de la URL sigue siendo 'prestamo_list' para no romper tus templates
    path('',                      prestamo_list_view, name='prestamo_list'), 
    path('crear/',                prestamo_create,   name='prestamo_create'),
    path('<int:pk>/editar/',      prestamo_edit,     name='prestamo_edit'),
    path('<int:pk>/eliminar/',    prestamo_delete,   name='prestamo_delete'),
    path('devoluciones/crear/',   devolucion_create, name='devolucion_create'),
]