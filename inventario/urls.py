from django.urls import path
from inventario.views import inventario, agregar_herramienta, editar_herramienta

urlpatterns = [
    path('',          inventario,           name='inventario'),
    path('agregar/',  agregar_herramienta,  name='agregar_herramienta'),
    path('editar/<int:pk>/', editar_herramienta, name='editar_herramienta'),
]