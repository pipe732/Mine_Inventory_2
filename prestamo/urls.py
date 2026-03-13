from django.urls import path
from . import views

urlpatterns = [

    # ── Usuarios ──────────────────────────────
    path('usuarios/',                       views.usuario_lista,    name='usuario_lista'),
    path('usuarios/crear/',                 views.usuario_crear,    name='usuario_crear'),
    path('usuarios/editar/<str:pk>/',       views.usuario_editar,   name='usuario_editar'),
    path('usuarios/eliminar/<str:pk>/',     views.usuario_eliminar, name='usuario_eliminar'),

    # ── Préstamos ─────────────────────────────
    path('prestamos/',                      views.prestamo_lista,   name='prestamo_lista'),
    path('prestamos/crear/',                views.prestamo_crear,   name='prestamo_crear'),
    path('prestamos/<int:pk>/',             views.prestamo_detalle, name='prestamo_detalle'),
    path('prestamos/editar/<int:pk>/',      views.prestamo_editar,  name='prestamo_editar'),
    path('prestamos/eliminar/<int:pk>/',    views.prestamo_eliminar,name='prestamo_eliminar'),

    # ── Detalles de Préstamo ──────────────────
    path('prestamos/<int:prestamo_pk>/agregar/',        views.detalle_prestamo_crear,    name='detalle_prestamo_crear'),
    path('detalles/eliminar/<int:pk>/',                 views.detalle_prestamo_eliminar, name='detalle_prestamo_eliminar'),

    # ── Devoluciones ──────────────────────────
    path('devoluciones/',                               views.devolucion_lista,   name='devolucion_lista'),
    path('devoluciones/crear/<int:detalle_pk>/',        views.devolucion_crear,   name='devolucion_crear'),
    path('devoluciones/eliminar/<int:pk>/',             views.devolucion_eliminar,name='devolucion_eliminar'),
]