from django.shortcuts import render, get_object_or_404, redirect
from .models import Stock, CategoriaHerramienta
from .forms import StockForm

def inventario(request):
    herramientas = Stock.objects.select_related('categoria').all()

    # Filtros
    q         = request.GET.get('q', '')
    estado    = request.GET.get('estado', '')
    categoria = request.GET.get('categoria', '')
    ubicacion = request.GET.get('ubicacion', '')

    if q:
        herramientas = herramientas.filter(herramienta__icontains=q) | \
                       herramientas.filter(codigo__icontains=q)
    if estado:
        herramientas = herramientas.filter(estado=estado)
    if categoria:
        herramientas = herramientas.filter(categoria_id=categoria)
    if ubicacion:
        herramientas = herramientas.filter(ubicacion__icontains=ubicacion)

    context = {
        'herramientas': herramientas,
        'categorias':   CategoriaHerramienta.objects.all(),
        'estados':      Stock.ESTADO_CHOICES,
        'filtros': {'q': q, 'estado': estado, 'categoria': categoria, 'ubicacion': ubicacion},
    }
    return render(request, 'inventario.html', context)


def agregar_herramienta(request):
    form = StockForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('inventario')
    return render(request, 'herramienta_form.html', {'form': form, 'titulo': 'Agregar herramienta'})


def editar_herramienta(request, pk):
    herramienta = get_object_or_404(Stock, pk=pk)
    form = StockForm(request.POST or None, instance=herramienta)
    if form.is_valid():
        form.save()
        return redirect('inventario')
    return render(request, 'herramienta_form.html', {'form': form, 'titulo': 'Editar herramienta'})