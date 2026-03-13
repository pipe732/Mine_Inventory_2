from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Fixed .py to .urls
    path('mine/', include('mine_inventory.urls')),
    path('prestamo/', include('prestamo.urls')), # Added URL pattern for prestamo app
    path('mantenimiento/', include('mantenimiento.urls')),#modulo de mantenimiento A L B E R T
    path('prestamo/', include('prestamo.urls')),
    path('inventario/', include('inventario.urls')),
    path('Usuario/', include('Usuario.urls')), # Added URL pattern for usuarios app
]