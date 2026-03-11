from django.urls import path
from . import views

urlpatterns = [

    path('', views.lista_mantenimiento, name='mantenimiento_list'),
    path('bitacora/', views.lista_bitacora, name='bitacora_list'),
    path('estado/', views.lista_estado, name='estado_list'),
    path('nuevo-estado/', views.crear_mantenimiento, name='mantenimiento_crear'),
    path('nuevo-mantenimiento/', views.crear_bitacora_mantenimiento, name='crear_bitacora_mantenimiento'),
]