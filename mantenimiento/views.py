from django.shortcuts import render, redirect
from .models import DetalleMantenimiento, BitacoraMantenimiento, BitacoraEstado
from .forms import BitacoraEstadoForm, BitacoraMantenimientoForm, DetalleMantenimientoForm

def lista_mantenimiento(request):
    detalles = DetalleMantenimiento.objects.all()
    return render(request, 'mantenimiento/mantenimiento.html', {'detalles': detalles})

def lista_bitacora(request):
    bitacoras = BitacoraMantenimiento.objects.all()
    return render(request, 'mantenimiento/bitacora.html', {'bitacoras': bitacoras})

def lista_estado(request):
    estados = BitacoraEstado.objects.all()
    return render(request, 'mantenimiento/estado.html', {'estados': estados})

#crear estado de herramientas
def crear_mantenimiento(request):
    if request.method == 'POST':
        form = BitacoraEstadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estado_list')
    else:
        form = BitacoraEstadoForm()
    return render(request, 'mantenimiento/crear_mantenimiento.html', {
        'form': form, 
        'titulo': 'Añadir Estado'
    })

#crear mantenimienetos con sus detalles
def crear_bitacora_mantenimiento(request):
    if request.method == 'POST':
        form_bitacora = BitacoraMantenimientoForm(request.POST)
        form_detalle = DetalleMantenimientoForm(request.POST)
        
        if form_bitacora.is_valid() and form_detalle.is_valid():
   
            bitacora = form_bitacora.save()
    
            detalle = form_detalle.save(commit=False)
     
            detalle.id_mantenimiento = bitacora 
   
            detalle.save()
            return redirect('mantenimiento_list')
    else:
        form_bitacora = BitacoraMantenimientoForm()
        form_detalle = DetalleMantenimientoForm()
    
    return render(request, 'mantenimiento/crear_mantenimiento.html', {
        'form_bitacora': form_bitacora,
        'form_detalle': form_detalle,
        'titulo': 'Registrar Nuevo Mantenimiento'
    })
    
