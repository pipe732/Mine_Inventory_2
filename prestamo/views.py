from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Prestamo, DetallePrestamo, DevolucionHerramienta, Estado
from inventario.models import Stock 

def prestamo_list_view(request):
    # Optimización de consultas
    qs = Prestamo.objects.select_related('id_estado', 'herramienta').prefetch_related('detalles')

    q      = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')

    if q:
        # Buscamos directamente en el CharField 'numero_documento'
        qs = qs.filter(numero_documento__icontains=q)
    if estado:
        qs = qs.filter(id_estado__id_estado=estado)

    paginator  = Paginator(qs, 10)
    prestamos  = paginator.get_page(request.GET.get('page', 1))

    context = {
        'prestamos':           prestamos,
        'estados':             Estado.objects.all(),
        # Enviamos el stock para poder seleccionarlo en el formulario de creación
        'herramientas':        Stock.objects.all(),
        'total_prestamos':     Prestamo.objects.count(),
        'prestamos_activos':   Prestamo.objects.filter(id_estado__nombre='Activo').count(),
        'prestamos_devueltos': Prestamo.objects.filter(id_estado__nombre='Devuelto').count(),
        'prestamos_vencidos':  Prestamo.objects.filter(id_estado__nombre='Vencido').count(),
    }
    return render(request, 'prestamo.html', context)


def prestamo_create(request):
    if request.method == 'POST':
        try:
            # 1. Obtener objetos necesarios
            estado = get_object_or_404(Estado, id_estado=request.POST['id_estado'])
            herramienta_principal = get_object_or_404(Stock, id_codigo=request.POST['id_herramienta'])
            
            # 2. Crear el Préstamo (Cabecera)
            p = Prestamo.objects.create(
                numero_documento=request.POST['numero_documento'], # Guardado como texto
                herramienta=herramienta_principal,
                id_estado=estado,
                observaciones=request.POST.get('observaciones', ''),
            )

            # 3. Crear los Detalles (si vienen en el formulario dinámico)
            herramientas_ids = request.POST.getlist('det_herramienta[]')
            cantidades = request.POST.getlist('det_cantidad[]')

            for h_id, cant in zip(herramientas_ids, cantidades):
                if h_id and cant:
                    h_obj = get_object_or_404(Stock, id_codigo=h_id)
                    DetallePrestamo.objects.create(
                        id_prestamo=p,
                        herramienta=h_obj,
                        cantidad=int(cant)
                    )
            
            messages.success(request, f'Préstamo #{p.id_prestamo} creado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear el préstamo: {e}')
            
    return redirect('prestamo_list')

def prestamo_edit(request, pk):
    p = get_object_or_404(Prestamo, pk=pk)
    if request.method == 'POST':
        try:
            p.numero_documento = request.POST['numero_documento']
            p.id_estado        = get_object_or_404(Estado, id_estado=request.POST['id_estado'])
            p.herramienta      = get_object_or_404(Stock, id_codigo=request.POST['id_herramienta'])
            p.observaciones    = request.POST.get('observaciones', '')
            p.save()
            messages.success(request, 'Préstamo actualizado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')
        return redirect('prestamo_list')
    
    return render(request, 'prestamo.html', {
        'prestamo': p, 
        'estados': Estado.objects.all(),
        'herramientas': Stock.objects.all()
    })

def prestamo_delete(request, pk):
    p = get_object_or_404(Prestamo, pk=pk)
    if request.method == 'POST':
        p.delete()
        messages.success(request, 'Préstamo eliminado.')
    return redirect('prestamo_list')

def devolucion_create(request):
    if request.method == 'POST':
        try:
            detalle = get_object_or_404(DetallePrestamo, pk=request.POST['id_detalle_prestamo'])
            herramienta = get_object_or_404(Stock, id_codigo=request.POST['id_herramienta'])
            
            DevolucionHerramienta.objects.create(
                id_detalle_prestamo=detalle,
                herramienta=herramienta,
                observaciones=request.POST.get('observaciones', ''),
            )
            
            # Cambiar estado a 'Devuelto' si existe ese estado
            estado_dev = Estado.objects.filter(nombre__icontains='Devuelto').first()
            if estado_dev:
                detalle.id_prestamo.id_estado = estado_dev
                detalle.id_prestamo.save()
                
            messages.success(request, 'Devolución registrada con éxito.')
        except Exception as e:
            messages.error(request, f'Error en la devolución: {e}')
    return redirect('prestamo_list')