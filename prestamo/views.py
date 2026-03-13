from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Usuario.models import Usuario          # ← U mayúscula
from .models import Prestamo, DetallePrestamo, DevolucionHerramienta, Estado
from inventario.models import Stock
# ═══════════════════════════════════════════
# USUARIO
# ═══════════════════════════════════════════

def usuario_lista(request):
    usuarios = Usuario.objects.select_related('id_rol').all()
    return render(request, 'usuarios/usuario_lista.html', {'usuarios': usuarios})


def usuario_crear(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('usuario_lista')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'titulo': 'Crear Usuario'})


def usuario_editar(request, pk):
    usuario = get_object_or_404(Usuario, numero_documento=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuario_lista')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'titulo': 'Editar Usuario'})


def usuario_eliminar(request, pk):
    usuario = get_object_or_404(Usuario, numero_documento=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('usuario_lista')
    return render(request, 'usuarios/usuario_confirmar_eliminar.html', {'usuario': usuario})


# ═══════════════════════════════════════════
# PRÉSTAMO
# ═══════════════════════════════════════════

def prestamo_lista(request):
    prestamos = Prestamo.objects.select_related('herramienta', 'id_estado').all()
    return render(request, 'prestamos/prestamo_lista.html', {'prestamos': prestamos})


def prestamo_crear(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Préstamo registrado correctamente.')
            return redirect('prestamo_lista')
    else:
        form = PrestamoForm()
    return render(request, 'prestamos/prestamo_form.html', {'form': form, 'titulo': 'Crear Préstamo'})


def prestamo_editar(request, pk):
    prestamo = get_object_or_404(Prestamo, id_prestamo=pk)
    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Préstamo actualizado correctamente.')
            return redirect('prestamo_lista')
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, 'prestamos/prestamo_form.html', {'form': form, 'titulo': 'Editar Préstamo'})


def prestamo_eliminar(request, pk):
    prestamo = get_object_or_404(Prestamo, id_prestamo=pk)
    if request.method == 'POST':
        prestamo.delete()
        messages.success(request, 'Préstamo eliminado correctamente.')
        return redirect('prestamo_lista')
    return render(request, 'prestamos/prestamo_confirmar_eliminar.html', {'prestamo': prestamo})


def prestamo_detalle(request, pk):
    """Vista de detalle: muestra el préstamo con todos sus detalles asociados."""
    prestamo = get_object_or_404(Prestamo, id_prestamo=pk)
    detalles = prestamo.detalles.select_related('herramienta').all()
    return render(request, 'prestamos/prestamo_detalle.html', {
        'prestamo': prestamo,
        'detalles': detalles,
    })


# ═══════════════════════════════════════════
# DETALLE DE PRÉSTAMO
# ═══════════════════════════════════════════

def detalle_prestamo_crear(request, prestamo_pk):
    prestamo = get_object_or_404(Prestamo, id_prestamo=prestamo_pk)
    if request.method == 'POST':
        form = DetallePrestamoForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.id_prestamo = prestamo
            detalle.save()
            messages.success(request, 'Herramienta agregada al préstamo.')
            return redirect('prestamo_detalle', pk=prestamo_pk)
    else:
        form = DetallePrestamoForm(initial={'id_prestamo': prestamo})
    return render(request, 'prestamos/detalle_form.html', {
        'form': form,
        'prestamo': prestamo,
        'titulo': 'Agregar Herramienta al Préstamo',
    })


def detalle_prestamo_eliminar(request, pk):
    detalle = get_object_or_404(DetallePrestamo, id_detalle_prestamo=pk)
    prestamo_pk = detalle.id_prestamo.id_prestamo
    if request.method == 'POST':
        detalle.delete()
        messages.success(request, 'Herramienta eliminada del préstamo.')
        return redirect('prestamo_detalle', pk=prestamo_pk)
    return render(request, 'prestamos/detalle_confirmar_eliminar.html', {'detalle': detalle})


# ═══════════════════════════════════════════
# DEVOLUCIÓN
# ═══════════════════════════════════════════

def devolucion_lista(request):
    devoluciones = DevolucionHerramienta.objects.select_related(
        'id_detalle_prestamo', 'herramienta'
    ).all()
    return render(request, 'prestamos/devolucion_lista.html', {'devoluciones': devoluciones})


def devolucion_crear(request, detalle_pk):
    detalle = get_object_or_404(DetallePrestamo, id_detalle_prestamo=detalle_pk)
    if request.method == 'POST':
        form = DevolucionHerramientaForm(request.POST)
        if form.is_valid():
            devolucion = form.save(commit=False)
            devolucion.id_detalle_prestamo = detalle
            devolucion.save()
            messages.success(request, 'Devolución registrada correctamente.')
            return redirect('devolucion_lista')
    else:
        form = DevolucionHerramientaForm(initial={
            'id_detalle_prestamo': detalle,
            'herramienta': detalle.herramienta,
        })
    return render(request, 'prestamos/devolucion_form.html', {
        'form': form,
        'detalle': detalle,
        'titulo': 'Registrar Devolución',
    })


def devolucion_eliminar(request, pk):
    devolucion = get_object_or_404(DevolucionHerramienta, id_devolucion_codigo=pk)
    if request.method == 'POST':
        devolucion.delete()
        messages.success(request, 'Devolución eliminada correctamente.')
        return redirect('devolucion_lista')
    return render(request, 'prestamos/devolucion_confirmar_eliminar.html', {'devolucion': devolucion})