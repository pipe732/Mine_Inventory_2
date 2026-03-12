from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Prestamo, DetallePrestamo, DevolucionHerramienta, Usuario, Estado


def prestamo(request):
    qs = Prestamo.objects.select_related('numero_documento', 'id_estado').prefetch_related('detalles')

    q      = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')

    if q:
        qs = qs.filter(
            Q(numero_documento__nombre_completo__icontains=q) |
            Q(numero_documento__numero_documento__icontains=q)
        )
    if estado:
        qs = qs.filter(id_estado__id_estado=estado)

    paginator  = Paginator(qs, 10)
    prestamos  = paginator.get_page(request.GET.get('page', 1))

    context = {
        'prestamos':           prestamos,
        'estados':             Estado.objects.all(),
        'usuarios':            Usuario.objects.all(),
        'total_prestamos':     Prestamo.objects.count(),
        'prestamos_activos':   Prestamo.objects.filter(id_estado__nombre='Activo').count(),
        'prestamos_devueltos': Prestamo.objects.filter(id_estado__nombre='Devuelto').count(),
        'prestamos_vencidos':  Prestamo.objects.filter(id_estado__nombre='Vencido').count(),
    }
    return render(request, 'prestamo.html', context)


def prestamo_create(request):
    if request.method == 'POST':
        try:
            usuario  = get_object_or_404(Usuario, numero_documento=request.POST['numero_documento'])
            estado   = get_object_or_404(Estado, id_estado=request.POST['id_estado'])
            p = Prestamo.objects.create(
                numero_documento=usuario,
                id_herramienta=request.POST['id_herramienta'],
                id_estado=estado,
                observaciones=request.POST.get('observaciones', ''),
            )
            for h, c in zip(request.POST.getlist('det_herramienta[]'), request.POST.getlist('det_cantidad[]')):
                if h and c:
                    DetallePrestamo.objects.create(id_prestamo=p, id_herramienta=int(h), cantidad=int(c))
            messages.success(request, f'Préstamo #{p.id_prestamo} creado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return redirect('prestamo_list')


def prestamo_edit(request, pk):
    p = get_object_or_404(Prestamo, pk=pk)
    if request.method == 'POST':
        p.numero_documento = get_object_or_404(Usuario, numero_documento=request.POST['numero_documento'])
        p.id_estado        = get_object_or_404(Estado, id_estado=request.POST['id_estado'])
        p.id_herramienta   = request.POST['id_herramienta']
        p.observaciones    = request.POST.get('observaciones', '')
        p.save()
        messages.success(request, 'Préstamo actualizado.')
        return redirect('prestamo_list')
    return render(request, 'prestamo.html', {'prestamo': p, 'estados': Estado.objects.all(), 'usuarios': Usuario.objects.all()})


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
            DevolucionHerramienta.objects.create(
                id_detalle_prestamo=detalle,
                id_herramienta=request.POST['id_herramienta'],
                observaciones=request.POST.get('observaciones', ''),
            )
            estado_dev = Estado.objects.filter(nombre='Devuelto').first()
            if estado_dev:
                detalle.id_prestamo.id_estado = estado_dev
                detalle.id_prestamo.save()
            messages.success(request, 'Devolución registrada.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return redirect('prestamo_list')
    
formset = DetallePrestamoFormSet(request.POST or None, instance=prestamo)
if prestamo_form.is_valid() and formset.is_valid():
    prestamo = prestamo_form.save()
    formset.instance = prestamo
    formset.save()